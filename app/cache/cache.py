import time

from config import config


class CustomCache(object):
    """
    Custom cache class for caching
    """

    def __init__(self):
        self.scenario_cache = {}
        self.scene_cache = {}
        self.asset_cache = {}
        self.scenario_name_to_id_cache = {}
        self.expire_time = config.get("cache.expire_time")

    async def check_and_get_scenario(self, scenario_id: str):
        ret_obj = None
        if scenario_id in self.scenario_cache:
            if self.scenario_cache[scenario_id]["timestamp"] + self.expire_time < int(
                time.time()
            ):
                del self.scenario_cache[scenario_id]
            else:
                ret_obj = self.scenario_cache[scenario_id]["obj_dict"]

        return ret_obj

    async def check_and_get_scenario_by_name(self, scenario_name: str):
        if scenario_name in self.scenario_name_to_id_cache:
            if self.scenario_name_to_id_cache[scenario_name][
                "timestamp"
            ] + self.expire_time < int(time.time()):
                del self.scenario_name_to_id_cache[scenario_name]
            else:
                scenario_id = self.scenario_name_to_id_cache[scenario_name]["id"]
                return await self.check_and_get_scenario(scenario_id)

        return None

    async def check_and_get_scene(self, scene_id: str):
        ret_obj = None
        if scene_id in self.scene_cache:
            if self.scene_cache[scene_id]["timestamp"] + self.expire_time < int(
                time.time()
            ):
                del self.scene_cache[scene_id]
            else:
                ret_obj = self.scene_cache[scene_id]["obj_dict"]

        return ret_obj

    async def check_and_get_asset(self, asset_id: str):
        ret_obj = None
        if asset_id in self.asset_cache:
            if self.asset_cache[asset_id]["timestamp"] + self.expire_time < int(
                time.time()
            ):
                del self.asset_cache[asset_id]
            else:
                ret_obj = self.asset_cache[asset_id]["obj_dict"]

        return ret_obj

    async def update_scenario_cache(self, id, scenario_obj_dict, scenario_name):
        cur_time = int(time.time())
        self.scenario_cache[id] = {
            "obj_dict": scenario_obj_dict,
            "timestamp": cur_time,
        }
        self.scenario_name_to_id_cache[scenario_name] = {
            "id": id,
            "timestamp": cur_time,
        }

    async def update_scene_cache(self, id, scene_obj_dict):
        self.scene_cache[id] = {
            "obj_dict": scene_obj_dict,
            "timestamp": int(time.time()),
        }

    async def update_asset_cache(self, id, asset_obj_dict):
        self.asset_cache[id] = {
            "obj_dict": asset_obj_dict,
            "timestamp": int(time.time()),
        }

    async def clear_all_cache(self):
        self.scenario_cache.clear()
        self.scene_cache.clear()
        self.asset_cache.clear()
        self.scenario_name_to_id_cache.clear()


CACHE = CustomCache()

check_and_get_scenario = CACHE.check_and_get_scenario

check_and_get_scenario_by_name = CACHE.check_and_get_scenario_by_name

check_and_get_scene = CACHE.check_and_get_scene

check_and_get_asset = CACHE.check_and_get_asset

clear_all_cache = CACHE.clear_all_cache

update_scenario_cache = CACHE.update_scenario_cache

update_scene_cache = CACHE.update_scene_cache

update_asset_cache = CACHE.update_asset_cache
