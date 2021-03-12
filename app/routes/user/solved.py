from library.postgres import get_solved_from_postgres
from routes.base import BaseUserAPIHandler


class UserSolvedHandler(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/solved/{id}
    """

    async def get(self, id):

        try:
            next_objects = await get_solved_from_postgres(id, self.session)
            await self.finish({"next_objects": next_objects})

        except ValueError:
            self.write_error(status_code=404, message="Object ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
