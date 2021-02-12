from app.library.postgres import get_text_from_postgres
from app.routes.base import BaseUserAPIHander


class UserTextHandler(BaseUserAPIHander):
    """
    Handle routes that have api/user/v1/text/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_text_from_postgres(id)
            await self.finish(response_dict)
        except ValueError:
            await self.write_error(status_code=404, message="Text ID not valid")
            return
        except Exception as e:
            await self.write_error(status_code=500, message=str(e))
