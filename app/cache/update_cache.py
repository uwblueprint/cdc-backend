import time
from datetime import datetime

from cache.cache import clear_all_cache, update_scenario_cache
from library.postgres import get_scene_from_postgres
from models import get_session
from models.db_client import get_scenarios


async def update_cache():
    session = get_session()
    await clear_all_cache()
    scenarios = get_scenarios(session)
    scenes_updated = set()
    for scenario in scenarios:
        await update_scenario_cache(
            scenario.id, scenario.as_dict(), scenario.friendly_name
        )
        for scene_id in scenario.scene_ids:
            if scene_id not in scenes_updated:
                await get_scene_from_postgres(
                    scene_id,
                    session,
                    update_cache=True,
                )
                scenes_updated.add(scene_id)

    print(datetime.fromtimestamp(int(time.time())), "Cache updated")
