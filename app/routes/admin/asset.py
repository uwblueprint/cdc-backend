import tornado.escape
from jsonschema import validate
from library.api_schemas import admin_asset_post_handler_schema
from library.postgres import post_asset_to_postgres
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
