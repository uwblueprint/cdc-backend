import boto3
import tornado.escape
from config import config
from jsonschema import validate
from library.api_schemas import (
    admin_object_handler_schema,
    admin_puzzle_delete_handler_schema,
    admin_puzzle_handler_schema,
)
from library.postgres import (
    clean_object_assets_from_aws,
    delete_object_in_postgres,
    get_object_from_postgres,
    post_object_to_postgres,
    update_object_in_postgres,
)
from routes.base import BaseAdminAPIHandler


class AdminObjectPostHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{scene_id}/object
    """

    async def post(self, scene_id):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_object_handler_schema)

            inserted_obj = await post_object_to_postgres(
                scene_id, data, self.db_session
            )

            await self.finish(inserted_obj)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminObjectPutHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{scene_id}/object/{object_id}
    """

    async def put(self, scene_id, object_id):
        # Validate that id is valid

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_object_handler_schema)

            response_message = await update_object_in_postgres(
                scene_id, object_id, data, self.db_session
            )
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def delete(self, scene_id, object_id):

        try:
            response_message = await delete_object_in_postgres(
                scene_id, object_id, self.db_session
            )
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminPuzzleHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{scene_id}/object/{object_id}/puzzle
    """

    async def get(self, scene_id, object_id):
        try:
            response_object = await get_object_from_postgres(object_id, self.db_session)
            response_message = {
                "name": response_object["name"],
                "animations_json": response_object["animations_json"],
                "is_interactable": response_object["is_interactable"],
            }
            await self.finish(response_message)
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def put(self, scene_id, object_id):
        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_puzzle_handler_schema)
            saved_object = await get_object_from_postgres(object_id, self.db_session)
            response_message = await update_object_in_postgres(
                scene_id, object_id, data, self.db_session
            )
            await clean_object_assets_from_aws(saved_object, response_message)

            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def post(self, scene_id, object_id):
        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_puzzle_delete_handler_schema)
            if (
                "aws" in config.get("app-env")
                and config.get("asset.aws_hard_delete", False)
                and len(data) > 0
            ):
                s3_client = boto3.client(
                    "s3",
                    endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                    region_name=config.get("s3.region"),
                )
                s3_client.delete_objects(
                    Bucket=config.get("s3.bucket_name"),
                    Delete={"Objects": [{"Key": a} for a in data]},
                )
                response = {"message": "Deleted successfully"}
                await self.finish(response)
            else:
                response = {"message": "Not set to be in delete mode, not deleted"}
                await self.finish(response)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
