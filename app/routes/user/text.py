from library.postgres import get_text_from_postgres
from routes.base import BaseUserAPIHandler


class UserTextHandler(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/text/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_text_from_postgres(id)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Text ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
