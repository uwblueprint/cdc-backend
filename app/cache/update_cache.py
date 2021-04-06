from models import get_session
from models.db_client import get_scenarios


async def update_cache():
    session = get_session()
    scenarios = get_scenarios(session)
    for scenario in scenarios:
        # TODO: include scenario's friendly_name from other PR in here
        # await update_scenario_cache(scenario.id, scenario.as_dict())
        pass
    # update scene cache
    # update asset cache
