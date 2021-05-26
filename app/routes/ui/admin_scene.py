import json

from config import config
from library.postgres import get_scene_from_postgres
from models import get_session
from routes.base import BaseAdminUIHandler


class UIAdminSceneHandler(BaseAdminUIHandler):
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
            )
        except ValueError as e:
            self.write_error(status_code=404, message=str(e))
        except Exception:
            # no need to expose exact exception error on this route
            self.write_error(status_code=500, message="Internal Server Error")
