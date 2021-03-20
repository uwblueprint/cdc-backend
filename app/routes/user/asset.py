from cache.cache import check_and_get_asset
from library.postgres import get_asset_from_postgres
from models import get_session
from routes.base import BaseUserAPIHandler


class UserAssetHandler(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/asset/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            # Check cache first
            response_dict = await check_and_get_asset(id)
            if not response_dict:
                self.db_session = get_session()
                response_dict = await get_asset_from_postgres(
                    id, self.db_session, update_cache=True
                )

            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
