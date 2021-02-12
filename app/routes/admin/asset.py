import tornado.escape
from config import config
from routes.base import BaseAdminAPIHandler


class AdminAssetHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/asset
    """

    async def post(self):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body

            if not data or "display_name" not in data or "object_type" not in data:
                raise ValueError("Missing required field.")

            if not data["display_name"].isalpha():
                raise ValueError("Validation failed for display name.")

            if not data["object_type"] in config.get("asset.allowed_asset_types"):
                raise ValueError("Validation failed for asset type")

            await self.finish("testttt")

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
