import base64
import io
import uuid

import boto3
import cv2
import tornado.escape
from botocore.config import Config
from config import config
from jsonschema import validate
from library.api_schemas import (
    admin_aws_handler_body_schema,
    admin_jigsaw_handler_body_schema,
)
from numpy import frombuffer, uint8
from routes.base import BaseAdminAPIHandler


class AdminUploadHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/[version]/upload
    """

    async def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_aws_handler_body_schema)

            default_fields = {"acl": "public-read"}
            default_conditions = [{"acl": "public-read"}]

            # if it's an image, we need to appropriately set the content-type so aframe can render it properly
            # not an issue for assets, since they are binary files.
            if data["type"] == "image" and "extension" in data:
                default_fields["Content-Type"] = "image/" + data["extension"]
                default_conditions.append(
                    {"Content-Type": "image/" + data["extension"]}
                )

            # if we are uploading a _new_ object, generate the s3 key based on prefix
            if "s3_key" not in data or data["s3_key"] == "":
                if data["type"] == "asset":
                    data["s3_key"] = "assets/" + uuid.uuid4().hex
                elif data["type"] == "image":
                    data["s3_key"] = "images/" + uuid.uuid4().hex
                else:
                    raise ValueError("Unsupported type attribute")

                if "extension" in data:
                    data["s3_key"] += "." + data["extension"]

            s3_client = boto3.client(
                "s3",
                config=Config(signature_version="s3v4"),
                endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                region_name=config.get("s3.region"),
            )
            resp = s3_client.generate_presigned_post(
                Bucket=config.get("s3.bucket_name"),
                Key=data["s3_key"],
                Fields=default_fields,
                Conditions=default_conditions,
                ExpiresIn=600,  # Expire URL in 10 minutes
            )
            resp["s3_key"] = data["s3_key"]
            await self.finish(resp)

        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminJigsawHelper(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/[version]/jigsaw
    """

    async def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_jigsaw_handler_body_schema)

            extra_args = {"ContentType": "image/png", "ACL": "public-read"}

            # read image and convert to format that cv2 expects
            nparr = frombuffer(base64.b64decode(data["encoded_image"]), uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            rows = data["rows"] if "rows" in data else 3
            columns = data["columns"] if "columns" in data else 3

            pixel_x_scale = int(img.shape[0] / rows)
            pixel_y_scale = int(img.shape[1] / columns)

            # Set up the S3 client for uploading
            s3_client = boto3.client(
                "s3",
                config=Config(signature_version="s3v4"),
                endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                region_name=config.get("s3.region"),
            )

            s3_key_prefix = "images/" + uuid.uuid4().hex + "-"
            s3_key_counter = 0
            s3_bucket_url = f"https://{config.get('s3.bucket_name')}.s3.{config.get('s3.region')}.amazonaws.com/"
            result_image_urls = []

            # Generate and upload to S3
            for r in range(1, rows + 1):
                for c in range(1, columns + 1):
                    _, buffer = cv2.imencode(
                        ".png",
                        img[
                            (r - 1) * pixel_x_scale : r * pixel_x_scale,  # noqa: E203
                            (c - 1) * pixel_y_scale : c * pixel_y_scale,  # noqa: E203
                        ],
                    )
                    io_buffer = io.BytesIO(buffer)
                    file_name = s3_key_prefix + str(s3_key_counter) + ".png"
                    s3_client.upload_fileobj(
                        Fileobj=io_buffer,
                        Bucket=config.get("s3.bucket_name"),
                        Key=file_name,
                        ExtraArgs=extra_args,
                    )
                    s3_key_counter += 1
                    result_image_urls.append(s3_bucket_url + file_name)

            response_dict = {"data": result_image_urls}
            await self.finish(response_dict)

        except Exception as e:
            self.write_error(status_code=500, message=str(e))
