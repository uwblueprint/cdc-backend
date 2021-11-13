from cache.cache import check_and_get_scenario_by_name
from config import config
from library.postgres import get_scenario_by_friendly_name_from_postgres
from models import get_session
from models.scenario import Scenario
from routes.base import BaseUIHandler


class UITutorialPageHandler(BaseUIHandler):
    """
    Handle routes that have {scenario_friendly_name}/tutorial
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
            if not scenario_obj.is_published and not scenario_obj.is_previewable:
                raise ValueError("This Scenario is currently not accessible")

            # Legacy code keeping for future, if we want to give the user a choice.
            # pan_mode = 0
            # try:
            #     pan_mode = int(self.get_argument("pan_mode", "0"))
            # except ValueError:
            #     pass

            await self.render(
                "tutorial.html",
                asset_prefix_url=config.get("asset.prefix_url"),
                scenario_name=scenario_obj.name,
                scenario_friendly_name=scenario_obj.friendly_name,
                # pan_mode="true" if pan_mode == 1 else "false",
            )
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception:
            # no need to expose exact exception error on this route
            self.write_error(status_code=500, message="Internal Server Error")
