from library.postgres import get_asset_from_postgres
from routes.base import BaseUserAPIHandler


class UserAssetHandler(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/asset/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_asset_from_postgres(id, self.db_session)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
