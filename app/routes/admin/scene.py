import tornado.escape
from jsonschema import validate
from library.api_schemas import (
    admin_scene_post_handler_schema,
    admin_scene_put_handler_schema,
)
from library.postgres import (
    duplicate_scene,
    get_scene_from_postgres,
    post_scene_to_postgres,
    update_scene_from_postgres,
)
from routes.base import BaseAdminAPIHandler


class AdminScenePostHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene
    """

    async def post(self):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_scene_post_handler_schema)

            id_inserted = await post_scene_to_postgres(data)

            await self.finish({"id": id_inserted})

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminSceneHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_scene_from_postgres(id)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Scene ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def put(self, id):
        # Validate that id is valid

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_scene_put_handler_schema)

            response_message = await update_scene_from_postgres(id, data)
            await self.finish(response_message)

        except ValueError:
            self.write_error(status_code=404, message="Scene ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminSceneDuplicateHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{id}/duplicate
    """

    async def post(self, id):

        try:

            response = await duplicate_scene(id)

            await self.finish(response)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
