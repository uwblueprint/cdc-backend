import json

from config import config
from library.postgres import get_scene_from_postgres
from models import get_session
from routes.base import BaseUIHandler


class UIAdminSceneHandler(BaseUIHandler):
    """
    Handle routes that have admin/scene/{scene_id}
    """

    async def get(self, scene_id):
        try:
            scene_id_int = int(scene_id)

            self.db_session = get_session()
            scene_dict = await get_scene_from_postgres(
                scene_id_int,
                self.db_session,
                update_cache=False,
            )

            background_ext = (
                "." + scene_dict["background_details"]["s3_key"].split(".")[-1]
            )
            navmesh_src = (
                scene_dict["background_details"]["s3_key"].removesuffix(background_ext)
                + "-navmesh"
                + ".gltf"
            )
            take_screenshot = False
            if (
                "screenshot_url" not in scene_dict
                or "scene-generic" in scene_dict["screenshot_url"]
            ):
                if "aws" in config.get("app-env"):
                    take_screenshot = True

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
                is_last_scene="false",
                is_admin=True,
                scenario_name="Edit Scene",
                scenario_friendly_name="friendly_name",
                scene_dict=scene_dict,
                asset_prefix_url=config.get("asset.prefix_url"),
                navmesh_src=navmesh_src,
                inspector_url=config.get("inspector_url"),
                json=json,
                cur_scene_idx=scene_id_int,
                take_screenshot=take_screenshot,
                next_scene_uri="irrelevant",
            )
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception:
            # no need to expose exact exception error on this route
            self.write_error(status_code=500, message="Internal Server Error")
