import tornado.escape
from jsonschema import validate
from library.api_schemas import admin_asset_post_handler_schema
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

            await self.finish("testttt")

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
