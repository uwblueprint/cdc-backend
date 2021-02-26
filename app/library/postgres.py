from models.asset import Asset
from models.db_client import (
    create_entity,
    get_asset,
    get_object,
    get_scenario,
    get_scene,
    get_text,
)
from models.object import Object
from models.scenario import Scenario
from models.scene import Scene
from models.text import Text


async def get_text_from_postgres(text_id: str):
    text_obj = get_text(text_id)
    if text_obj is None:
        raise ValueError("Invalid Text ID")

    return text_obj.as_dict()


async def get_solved_from_postgres(object_id: str):
    object_obj = await get_object_from_postgres(object_id)

    return object_obj["next_objects"]


async def post_asset_to_postgres(data: dict):
    asset_model = Asset(**data)
    asset_model = create_entity(asset_model)

    return asset_model.as_dict()


async def get_object_from_postgres(object_id: str):
    object_obj = get_object(object_id)
    if object_obj is None:
        raise ValueError("Object ID not valid")

    return object_obj.as_dict()


async def get_scene_from_postgres(scene_id: str):
    scene_obj = get_scene(scene_id)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    response = scene_obj.as_dict()

    objects = []
    for object_id in response["object_ids"]:
        objects.append(await get_object_from_postgres(object_id))

    response["objects"] = objects
    return response


async def get_loading_screen_from_postgres():
    # TODO: get actual loading scene from postgres once we have it
    return await get_scene_from_postgres("123")


async def get_asset_from_postgres(asset_id: str):
    asset_obj = get_asset(asset_id)
    if asset_obj is None:
        raise ValueError("Asset ID not valid")

    return asset_obj.as_dict()


async def delete_asset_from_postgres(asset_id: str):
    # TODO: delete from postgres

    sample_response = {"message": "deleted successfully"}
    return sample_response


async def update_asset_from_postgres(asset_id: str, data: dict):
    # TODO: update item into postgres

    sample_response = {"message": "updated asset with id " + asset_id}
    return sample_response  # Represents id


async def post_scenario_to_postgres(data: dict):
    scenario_obj = Scenario(**data)
    scenario_obj = create_entity(scenario_obj)
    return scenario_obj.as_dict()


async def get_scenario_from_postgres(scenario_id: str):
    scenario_obj = get_scenario(scenario_id)
    if scenario_obj is None:
        raise ValueError("Scenario ID not valid")

    return scenario_obj.as_dict()


async def delete_scenario_from_postgres(scenario_id: str):
    # TODO: delete from postgres

    sample_response = {"message": "deleted successfully"}
    return sample_response


async def update_scenario_from_postgres(scenario_id: str, data: dict):
    # TODO: update item into postgres

    sample_response = {"message": "updated scenario with id " + scenario_id}
    return sample_response  # Represents id


async def post_scene_to_postgres(data: dict):
    scene_model = Scene(**data)
    scene_model = create_entity(scene_model)
    return scene_model.as_dict()


async def update_scene_from_postgres(scene_id: str, data: dict):
    # TODO: update item into postgres

    sample_response = {"message": "updated scene with id " + scene_id}
    return sample_response  # Represents id


async def duplicate_scenario(scenario_id: str):
    # TODO: actual duplication in postgres
    sample_response = {
        "message": "Duplicated scenario with id " + scenario_id,
        "id": scenario_id + "2",
    }
    return sample_response


async def duplicate_scene(scene_id: str):
    # TODO: actual duplication in postgres
    sample_response = {
        "message": "Duplicated scene with id " + scene_id,
        "id": scene_id + "3",
    }
    return sample_response


async def post_object_to_postgres(scene_id: str, data: dict):
    object_model = Object(**data)
    object_model = create_entity(object_model)

    return object_model.as_dict()


async def update_object_in_postgres(scene_id: str, object_id: str, data: dict):
    # TODO add object to postgres
    # TODO add object id to scene's list of objects
    return await get_object_from_postgres(object_id)


async def post_text_to_postgres(scene_id: str, data: dict):
    text_obj = Text(**data)
    text_obj = create_entity(text_obj)

    return text_obj.as_dict()


async def put_text_to_postgres(scene_id: str, text_id: str, data: dict):
    # TODO: actual PUT to postgres
    return {"sample": "response"}


async def delete_text_from_postgres(scene_id: str, text_id: str, data: dict):
    # TODO: actual DELETE from postgres
    return {"sample": "response"}
