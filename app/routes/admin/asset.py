import tornado.escape
from jsonschema import validate
from library.api_schemas import admin_asset_post_handler_schema
from library.postgres import get_asset_from_postgres, post_asset_to_postgres
from routes.base import BaseAdminAPIHandler


class AdminAssetPostHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/asset
    """

    async def post(self):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_asset_post_handler_schema)

            id_inserted = await post_asset_to_postgres(data)

            await self.finish({"id": id_inserted})

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminAssetHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/asset/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_asset_from_postgres(id)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
