from cache.cache import update_asset_cache, update_scenario_cache, update_scene_cache
from models.asset import Asset
from models.db_client import (
    create_entity,
    delete_asset,
    delete_object,
    delete_scenario,
    delete_scene,
    get_asset,
    get_assets,
    get_object,
    get_scenario,
    get_scenario_by_friendly_name,
    get_scenarios,
    get_scene,
    get_scenes,
    put_asset,
    put_object,
    put_scenario,
    put_scene,
)
from models.object import Object
from models.scenario import Scenario
from models.scene import Scene


async def get_solved_from_postgres(object_id: str, session):
    object_obj = await get_object_from_postgres(object_id, session)

    return object_obj["next_objects"]


async def post_asset_to_postgres(data: dict, session):
    asset_model = Asset(**data)
    asset_model = create_entity(asset_model, session)

    return asset_model.as_dict()


async def get_object_from_postgres(object_id: str, session, update_cache=False):
    object_obj = get_object(object_id, session)
    if object_obj is None:
        raise ValueError("Object ID not valid")
    object_obj_dict = object_obj.as_dict()

    # Get the asset details
    object_obj_dict["asset_details"] = await get_asset_from_postgres(
        object_obj.asset_id, session, update_cache
    )

    return object_obj_dict


async def get_scene_from_postgres(scene_id: str, session, update_cache=False):
    scene_obj = get_scene(scene_id, session)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    response = scene_obj.as_dict()

    objects = []
    for object_id in response["object_ids"]:
        objects.append(await get_object_from_postgres(object_id, session, update_cache))

    response["objects"] = objects
    response["background_details"] = await get_asset_from_postgres(
        scene_obj.background_id, session, update_cache
    )

    if update_cache:
        await update_scene_cache(scene_id, response)
    return response


async def get_scenes_from_postgres(session):
    scenes = get_scenes(session)
    resp_dict = {"scenes": [scene.as_dict() for scene in scenes]}
    return resp_dict


async def get_loading_screen_from_postgres(session):
    # TODO: get actual loading scene from postgres once we have it
    return await get_scene_from_postgres("123", session)


async def get_asset_from_postgres(asset_id: str, session, update_cache=False):
    asset_obj = get_asset(asset_id, session)
    if asset_obj is None:
        raise ValueError("Asset ID not valid")

    response = asset_obj.as_dict()
    if update_cache:
        await update_asset_cache(asset_id, response)

    return response


async def get_assets_from_postgres(session):
    assets = get_assets(session)
    resp_dict = {"assets": [asset.as_dict() for asset in assets]}
    return resp_dict


async def delete_asset_from_postgres(asset_id: str, session):
    if not delete_asset(asset_id, session):
        raise ValueError("Asset ID not valid")

    response = {"message": "Deleted successfully"}
    return response


async def update_asset_from_postgres(asset_id: str, data: dict, session):
    num_assets_updated = put_asset(asset_id, data, session)
    if num_assets_updated == 0:
        raise ValueError("Invalid Asset ID")
    return await get_asset_from_postgres(asset_id, session)


async def post_scenario_to_postgres(data: dict, session):
    scenario_obj = Scenario(**data)
    potential_duplicate = get_scenario_by_friendly_name(
        scenario_obj.friendly_name, session
    )
    if potential_duplicate is not None:
        # this friendly name already exists
        raise AssertionError("Scenario with that friendly name already exists")
    scenario_obj = create_entity(scenario_obj, session)
    return scenario_obj.as_dict()


async def get_scenario_from_postgres(scenario_id: str, session, update_cache=False):
    scenario_obj = get_scenario(scenario_id, session)
    if scenario_obj is None:
        raise ValueError("Scenario ID not valid")
    scenario_obj_dict = scenario_obj.as_dict()
    if update_cache:
        await update_scenario_cache(
            scenario_id, scenario_obj_dict, scenario_obj.friendly_name
        )
    return scenario_obj_dict


async def get_scenarios_from_postgres(session):
    scenarios = get_scenarios(session)
    resp_dict = {"scenarios": [scenario.as_dict() for scenario in scenarios]}
    return resp_dict


async def get_scenario_by_friendly_name_from_postgres(
    friendly_name: str, session, update_cache=False
):
    scenario_obj: Scenario = get_scenario_by_friendly_name(friendly_name, session)
    if scenario_obj is None:
        raise ValueError("Unknown Scenario")
    if update_cache:
        await update_scenario_cache(
            scenario_obj.id, scenario_obj.as_dict(), scenario_obj.friendly_name
        )
    return scenario_obj


async def delete_scenario_from_postgres(scenario_id: str, session):
    if not delete_scenario(scenario_id, session):
        raise ValueError("Scenario ID not valid")

    response = {"message": "Deleted successfully"}
    return response


async def update_scenario_from_postgres(scenario_id: str, data: dict, session):
    potential_duplicate: Scenario = get_scenario_by_friendly_name(
        data["friendly_name"], session
    )
    if potential_duplicate is not None:
        # this friendly name already exists, ensure it is the current scenario
        if potential_duplicate.id != int(scenario_id):
            raise AssertionError("Scenario with that friendly name already exists")

    num_scenarios_updated = put_scenario(scenario_id, data, session)
    if num_scenarios_updated == 0:
        raise ValueError("Invalid Scenario ID")
    return await get_scenario_from_postgres(scenario_id, session)


async def post_scene_to_postgres(data: dict, session):
    scene_model = Scene(**data)
    scene_model = create_entity(scene_model, session)
    return scene_model.as_dict()


async def update_scene_from_postgres(scene_id: str, data: dict, session):
    num_scenes_updated = put_scene(scene_id, data, session)
    if num_scenes_updated == 0:
        raise ValueError("Invalid scene ID")
    return await get_scene_from_postgres(scene_id, session)


async def delete_scene_from_postgres(scene_id: str, session):
    # Get scene first
    scene_obj: Scene = get_scene(scene_id, session)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    # Delete all objects in the scene
    for object_id in scene_obj.object_ids:
        await delete_object_in_postgres(scene_id, object_id, session)

    # Delete the scene
    if not delete_scene(scene_id, session):
        raise ValueError("Scene ID not valid")

    # Remove the scene from scenario's scene_ids array
    scenarios = get_scenarios(session)
    for scenario in scenarios:
        if int(scene_id) in scenario.scene_ids:
            scenario_obj: Scenario = await get_scenario_from_postgres(
                scenario.id, session
            )
            scenario_obj["scene_ids"].remove(int(scene_id))
            await update_scenario_from_postgres(scenario.id, scenario_obj, session)

    response = {"message": "Deleted successfully"}
    return response


async def duplicate_scenario(scenario_id: str, session):
    # TODO: actual duplication in postgres
    sample_response = {
        "message": "Duplicated scenario with id " + scenario_id,
        "id": scenario_id + "2",
    }
    return sample_response


async def duplicate_scene(scene_id: str, session):
    # TODO: actual duplication in postgres
    sample_response = {
        "message": "Duplicated scene with id " + scene_id,
        "id": scene_id + "3",
    }
    return sample_response


async def post_object_to_postgres(scene_id: str, data: dict, session):
    object_model = Object(**data)

    # Ensure each object exists and it is either an object, as postgres won't do validation for us
    for next_obj in object_model.next_objects:
        try:
            await get_object_from_postgres(next_obj["id"], session)
        except KeyError:
            raise ValueError("one of the objects in next_objects is missing id")
        except ValueError:
            raise ValueError(
                "one of the objects in next_objects refers to an invalid id"
            )

    # Make sure the scene exists
    scene_obj: Scene = get_scene(scene_id, session)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    object_model = create_entity(object_model, session)

    # Add object to the scene
    scene_obj.object_ids.append(object_model.id)
    put_scene(scene_id, scene_obj.as_dict(), session)

    return object_model.as_dict()


async def update_object_in_postgres(scene_id: str, object_id: str, data: dict, session):
    num_objects_updated = put_object(object_id, data, session)
    if num_objects_updated == 0:
        raise ValueError("Invalid Object ID")

    return await get_object_from_postgres(object_id, session)


async def delete_object_in_postgres(scene_id: str, object_id: str, session):
    # Make sure the scene exists
    scene_obj: Scene = get_scene(scene_id, session)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    if not delete_object(object_id, session):
        raise ValueError("Object ID not valid")

    # Remove object from the scene
    if int(object_id) in scene_obj.object_ids:
        scene_obj.object_ids.remove(int(object_id))
        put_scene(scene_id, scene_obj.as_dict(), session)

    response = {"message": "Deleted successfully"}
    return response
