from cache.cache import check_and_get_scenario
from library.postgres import get_scenario_from_postgres
from models import get_session
from routes.base import BaseUserAPIHandler


class UserScenarioHandler(BaseUserAPIHandler):
    """
    Handle routes that have api/user/v1/scenario/{id}
    """

    async def get(self, id):
        # Validate that id is valid

        try:
            # Check cache first
            scenario_obj = await check_and_get_scenario(id)
            if not scenario_obj:
                self.db_session = get_session()
                scenario_obj = await get_scenario_from_postgres(
                    id, self.db_session, update_cache=True
                )
            await self.finish(scenario_obj)

        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            self.write_error(status_code=500, message=str(e))
