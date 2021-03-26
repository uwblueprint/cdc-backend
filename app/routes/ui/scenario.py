from routes.base import BaseUIHandler


class UIScenarioHandler(BaseUIHandler):
    """
    Handle routes that have {scenario_friendly_name}/{scene_number}
    """

    async def get(self, scenario_friendly_name, scene_number=1):
        try:
            scene_number_int = int(scene_number)
            await self.finish(
                {
                    "scenario": scenario_friendly_name,
                    "scene_num": scene_number_int,
                }
            )
        except Exception:
            self.write_error(status_code=500, message="Internal Server Error")
