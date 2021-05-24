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

            # if we are uploading a _new_ object, generate the s3 key based on prefix
            if "s3_key" not in data or data["s3_key"] == "":
                if data["type"] == "asset":
                    data["s3_key"] = "assets/" + uuid.uuid4().hex
                elif data["type"] == "image":
                    data["s3_key"] = "images/" + uuid.uuid4().hex
                else:
                    raise ValueError("Unsupported type attribute")

            s3_client = boto3.client(
                "s3",
                config=Config(signature_version="s3v4"),
                endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                region_name=config.get("s3.region"),
            )
            resp = s3_client.generate_presigned_post(
                Bucket=config.get("s3.bucket_name"),
                Key=data["s3_key"],
                Fields={"acl": "public-read"},
                Conditions=[{"acl": "public-read"}],
                ExpiresIn=600,  # Expire URL in 10 minutes
            )
            resp["s3_key"] = data["s3_key"]
            await self.finish(resp)

        except Exception as e:
            self.write_error(status_code=500, message=str(e))
