from library.postgres import get_scene_from_postgres
from routes.base import BaseUserAPIHandler


class UserSceneHandler(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/scene/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_scene_from_postgres(id, self.db_session)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
