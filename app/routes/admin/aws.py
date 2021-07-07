import uuid

import boto3
import tornado.escape
from botocore.config import Config
from config import config
from jsonschema import validate
from library.api_schemas import admin_aws_handler_body_schema
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
