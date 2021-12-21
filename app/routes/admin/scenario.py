import boto3
import tornado.escape
from config import config
from jsonschema import validate
from library.api_schemas import (
    admin_scenario_post_handler_schema,
    admin_scenario_put_handler_schema,
    admin_transition_image_delete_handler_schema,
)
from library.postgres import (
    delete_scenario_from_postgres,
    duplicate_scenario,
    get_scenario_from_postgres,
    get_scenarios_from_postgres,
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

            scenario_obj = await post_scenario_to_postgres(data, self.db_session)

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
            scenario_obj = await get_scenario_from_postgres(id, self.db_session)
            await self.finish(scenario_obj)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def delete(self, id):
        # Validate that id is valid

        try:
            response_message = await delete_scenario_from_postgres(id, self.db_session)
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))

    async def put(self, id):
        # Validate that id is valid

        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_scenario_put_handler_schema)

            response_message = await update_scenario_from_postgres(
                id, data, self.db_session
            )
            await self.finish(response_message)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminScenarioDuplicateHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scenario/{id}/duplicate
    """

    async def post(self, id):

        try:

            response = await duplicate_scenario(id, self.db_session)

            await self.finish(response)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminScenariosHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/[version]/scenarios
    """

    async def get(self):
        try:
            response_dict = await get_scenarios_from_postgres(self.db_session)
            await self.finish(response_dict)

        except Exception as e:
            self.write_error(status_code=500, message=str(e))


class AdminScenarioTransitionHandler(BaseAdminAPIHandler):
    """
    Handle routes that have api/admin/v1/scenario/{id}/transition
    """

    async def post(self, id):
        try:
            data = tornado.escape.json_decode(self.request.body)

            # validate body
            validate(data, schema=admin_transition_image_delete_handler_schema)
            if (
                "aws" in config.get("app-env")
                and config.get("asset.aws_hard_delete", False)
                and len(data) > 0
            ):
                s3_client = boto3.client(
                    "s3",
                    endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                    region_name=config.get("s3.region"),
                )
                s3_client.delete_objects(
                    Bucket=config.get("s3.bucket_name"),
                    Delete={"Objects": [{"Key": a} for a in data]},
                )

                response = {"message": "Deleted successfully"}
                await self.finish(response)
            else:
                response = {"message": "Not set to be in delete mode, not deleted"}
                await self.finish(response)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
