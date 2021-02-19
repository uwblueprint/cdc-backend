import tornado.escape
from jsonschema import validate
from library.api_schemas import admin_scenario_handler_body_schema
from library.postgres import post_scenario_to_postgres
from routes.base import BaseAdminAPIHandler


class AdminScenarioPostHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scenario
    """

    async def post(self):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_scenario_handler_body_schema)

            id_inserted = await post_scenario_to_postgres(data)

            await self.finish({"id": id_inserted})

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


"""
class AdminScenarioHandler(BaseAdminAPIHandler):

    Handle routes that have api/admin/v1/asset/{id}


    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_asset_from_postgres(id)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def delete(self, id):
        # Validate that id is valid

        try:
            response_message = await delete_asset_from_postgres(id)
            await self.finish(response_message)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def put(self, id):
        # Validate that id is valid

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_asset_handler_body_schema)

            response_message = await update_asset_from_postgres(id, data)
            await self.finish(response_message)

        except ValueError:
            self.write_error(status_code=404, message="Asset ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
"""
