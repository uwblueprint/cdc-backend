import tornado.escape
from jsonschema import validate
from library.api_schemas import (
    admin_scene_post_handler_schema,
    admin_scene_put_handler_schema,
    admin_screenshot_handler,
)
from library.postgres import (
    delete_scene_from_postgres,
    duplicate_scene,
    get_scene_from_postgres,
    get_scenes_from_postgres,
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

            scene_dict = await post_scene_to_postgres(data, self.db_session)

            await self.finish(scene_dict)

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
            response_dict = await get_scene_from_postgres(id, self.db_session)
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

            response_message = await update_scene_from_postgres(
                id, data, self.db_session
            )
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def delete(self, id):
        # Validate that id is valid

        try:
            response_message = await delete_scene_from_postgres(id, self.db_session)
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminSceneDuplicateHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{id}/duplicate
    """

    async def post(self, id):

        try:

            response = await duplicate_scene(id, self.db_session)

            await self.finish(response)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminScenesHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/[version]/scenes
    """

    async def get(self):
        try:
            response_dict = await get_scenes_from_postgres(self.db_session)
            await self.finish(response_dict)

        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminSceneScreenshotHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scene/{id}/screenshot
    """

    async def put(self, id):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_screenshot_handler)

            response_message = await update_scene_from_postgres(
                id, data, self.db_session
            )
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
