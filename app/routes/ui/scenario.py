from config import config
from library.postgres import (
    get_scenario_by_friendly_name_from_postgres,
    get_scene_from_postgres,
)
from models.scenario import Scenario
from routes.base import BaseUIHandler


class UIScenarioHandler(BaseUIHandler):
    """
    Handle routes that have {scenario_friendly_name}/{scene_number}
    """

    async def get(self, scenario_friendly_name, scene_number=0):
        try:
            scene_number_int = int(scene_number)
            # TODO: caching will be dealt with in a later PR
            scenario_obj: Scenario = await get_scenario_by_friendly_name_from_postgres(
                scenario_friendly_name, self.db_session
            )
            if not scenario_obj.is_published:
                raise ValueError("This Scenario is currently not accessible")

            if scene_number_int >= len(scenario_obj.scene_ids) or scene_number_int < 0:
                raise ValueError("Invalid Scene")

            # TODO: caching will be dealt with in a later PR
            scene_dict = await get_scene_from_postgres(
                scenario_obj.scene_ids[scene_number_int], self.db_session
            )

            is_last_scene = scene_number_int == len(scenario_obj.scene_ids) - 1

            await self.render(
                "scene.html",
                is_last_scene=is_last_scene,
                scenario_dict=scenario_obj.as_dict(),
                scene_dict=scene_dict,
                asset_prefix_url=config.get("asset.prefix_url"),
            )
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception as e:
            # no need to expose exact exception error on this route
            print(str(e))
            self.write_error(status_code=500, message="Internal Server Error")
