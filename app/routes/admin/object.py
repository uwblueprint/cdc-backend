import tornado.escape
from jsonschema import validate
from library.api_schemas import admin_object_handler_schema
from library.postgres import (
    delete_object_in_postgres,
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
