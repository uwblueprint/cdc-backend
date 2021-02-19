from library.postgres import get_loading_screen_from_postgres
from routes.base import BaseUserAPIHandler


class UserLoadingScreen(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/loading_screen
    """

    async def get(self):
        # Validate that id is valid

        try:
            response_dict = await get_loading_screen_from_postgres()
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
