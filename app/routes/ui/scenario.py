from routes.base import BaseUIHandler


class UIScenarioHandler(BaseUIHandler):
    """
    Handle routes that have {scenario_friendly_name}/{scene_number}
    """

    async def get(self, scenario_friendly_name, scene_number=None):
        pass
