import tornado.escape
from jsonschema import validate
from library.api_schemas import admin_text_handler_schema
from library.postgres import post_text_to_postgres, put_text_to_postgres
from routes.base import BaseAdminAPIHandler


class AdminTextPostHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{scene_id}/text
    """

    async def post(self, scene_id):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_text_handler_schema)

            inserted_obj = await post_text_to_postgres(scene_id, data)

            await self.finish(inserted_obj)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminTextPutHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{scene_id}/text/{text_id}
    """

    async def put(self, scene_id, text_id):
        # Validate that id is valid

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_text_handler_schema)

            response_message = await put_text_to_postgres(scene_id, text_id, data)
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))