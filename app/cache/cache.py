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

    async def check_and_get_scene(self, scene_id: str):
        pass

    async def check_and_get_asset(self, asset_id: str):
        pass

    async def update_scenario_cache(self, id, scenario_obj_dict):
        self.scenario_cache[id] = {
            "obj_dict": scenario_obj_dict,
            "timestamp": int(time.time()),
        }


CACHE = CustomCache()

check_and_get_scenario = CACHE.check_and_get_scenario

check_and_get_scene = CACHE.check_and_get_scene

check_and_get_asset = CACHE.check_and_get_asset

update_scenario_cache = CACHE.update_scenario_cache
