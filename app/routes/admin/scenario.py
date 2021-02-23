import tornado.escape
from jsonschema import validate
from library.api_schemas import (
    admin_scenario_post_handler_schema,
    admin_scenario_put_handler_schema,
)
from library.postgres import (
    delete_scenario_from_postgres,
    duplicate_scenario,
    get_scenario_from_postgres,
    post_scenario_to_postgres,
    update_scenario_from_postgres,
)
from routes.base import BaseAdminAPIHandler


class AdminScenarioPostHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scenario
    """

    async def post(self):

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_scenario_post_handler_schema)

            scenario_obj = await post_scenario_to_postgres(data)

            await self.finish(scenario_obj)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminScenarioHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scenario/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            response_dict = await get_scenario_from_postgres(id)
            await self.finish(response_dict)

        except ValueError:
            self.write_error(status_code=404, message="Scenario ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def delete(self, id):
        # Validate that id is valid

        try:
            response_message = await delete_scenario_from_postgres(id)
            await self.finish(response_message)

        except ValueError:
            self.write_error(status_code=404, message="Scenario ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def put(self, id):
        # Validate that id is valid

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_scenario_put_handler_schema)

            response_message = await update_scenario_from_postgres(id, data)
            await self.finish(response_message)

        except ValueError:
            self.write_error(status_code=404, message="Scenario ID not valid")
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminScenarioDuplicateHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scenario/{id}/duplicate
    """

    async def post(self, id):

        try:

            response = await duplicate_scenario(id)

            await self.finish(response)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
