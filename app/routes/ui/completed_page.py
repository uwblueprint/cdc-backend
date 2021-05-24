from cache.cache import check_and_get_scenario_by_name
from library.postgres import get_scenario_by_friendly_name_from_postgres
from models import get_session
from models.scenario import Scenario
from routes.base import BaseUIHandler


class UIScenarioCompletedPageHandler(BaseUIHandler):
    """
    Handle routes that have {scenario_friendly_name}/completed
    """

    async def get(self, scenario_friendly_name):
        try:
            scenario_dict = await check_and_get_scenario_by_name(scenario_friendly_name)
            if not scenario_dict:
                if not self.db_session:
                    self.db_session = get_session()
                scenario_obj: Scenario = (
                    await get_scenario_by_friendly_name_from_postgres(
                        scenario_friendly_name, self.db_session, update_cache=True
                    )
                )
            else:
                scenario_obj: Scenario = Scenario(**scenario_dict)
            if not scenario_obj.is_published:
                raise ValueError("This Scenario is currently not accessible")

            await self.render(
                "completed_page.html",
                scenario_name=scenario_obj.name,
                scenario_conclusion_data=scenario_obj.conclusion_data,
            )
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception:
            # no need to expose exact exception error on this route
            self.write_error(status_code=500, message="Internal Server Error")
