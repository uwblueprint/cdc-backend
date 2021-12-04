import json

from cache.cache import check_and_get_scenario_by_name, check_and_get_scene
from config import config
from library.postgres import (
    get_scenario_by_friendly_name_from_postgres,
    get_scene_from_postgres,
)
from models import get_session
from models.scenario import Scenario
from routes.base import BaseUIHandler


class UIScenarioHandler(BaseUIHandler):
    """
    Handle routes that have {scenario_friendly_name}/{scene_number}
    """

    async def get(self, scenario_friendly_name, scene_number=0):
        try:
            scene_number_int = int(scene_number)
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

            if scene_number_int >= len(scenario_obj.scene_ids) or scene_number_int < 0:
                raise ValueError("Invalid Scene")

            scene_dict = await check_and_get_scene(
                scenario_obj.scene_ids[scene_number_int]
            )
            if not scene_dict:
                if not self.db_session:
                    self.db_session = get_session()
                scene_dict = await get_scene_from_postgres(
                    scenario_obj.scene_ids[scene_number_int],
                    self.db_session,
                    update_cache=True,
                )

            # Need to convert to JS version of True/False
            is_last_scene = (
                "true"
                if (scene_number_int == len(scenario_obj.scene_ids) - 1)
                else "false"
            )
            background_ext = (
                "." + scene_dict["background_details"]["s3_key"].split(".")[-1]
            )
            navmesh_src = (
                scene_dict["background_details"]["s3_key"].removesuffix(background_ext)
                + "-navmesh"
                + ".gltf"
            )

            # Need to special parsing for hints
            hints_array = [{"text": x} for x in scene_dict["hints"]]
            hints_array.insert(
                -1,
                {
                    "text": "The next panel contains the solution to the current room, only proceed if you want to "
                    "view the answer!",
                    "imageSrc": "/static/img/spoiler.jpeg",
                },
            )
            scene_dict["hint_obj"] = {
                "jsonData": {"data": hints_array, "currPosition": 0},
                "componentType": "text-pane",
            }

            await self.render(
                "scene.html",
                is_last_scene=is_last_scene,
                is_admin=False,
                scenario_name=scenario_obj.name,
                scenario_friendly_name=scenario_obj.friendly_name,
                scene_dict=scene_dict,
                asset_prefix_url=config.get("asset.prefix_url"),
                navmesh_src=navmesh_src,
                json=json,
                cur_scene_idx=scene_number_int,
                scenario_transitions=scenario_obj.transitions,
                take_screenshot=False,
            )
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception:
            # no need to expose exact exception error on this route
            self.write_error(status_code=500, message="Internal Server Error")
