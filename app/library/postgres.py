from models.asset import Asset
from models.db_client import create_entity, get_asset, get_text
from models.scenario import Scenario


async def get_text_from_postgres(text_id: str):
    text_obj = get_text(text_id)
    if text_obj is None:
        raise ValueError("Invalid Text ID")

    return text_obj.as_dict()


async def get_solved_from_postgres(object_id: str):
    # TODO: Get actual list from postgres

    next_object_ids = ["1", "2", "23", "37", object_id]
    return next_object_ids


async def post_asset_to_postgres(data: dict):
    asset_model = Asset(**data)
    asset_model = create_entity(asset_model)

    return asset_model.as_dict()


async def get_object_from_postgres(object_id: str):
    # TODO: get datta from SQL -> model representation?

    sample_response = {
        "object_id": object_id,
        "position": [1.1, 1.5, 1.1],
        "scale": [1.0, 1.0, 1.0],
        "rotation": [0.1, 0.5, 0.1],
        "asset_id": 2,
        "next_objects": [3],
        "text_id": 3,
        "is_interactable": True,
        "animations_json": {},
    }
    return sample_response


async def get_scene_from_postgres(scene_id: str):
    # TODO: get datta from SQL -> model representation?

    # NOTE: scene response should populate the objects properly by getting object from postgres
    # TODO: get actual camera properties
    sample_response = {
        "id": scene_id,
        "name": "Master Bedroom",
        "description": "A standard master bedroom. King size bed, a dresser, ensuit washroom, and a large closet.",
        "object_ids": [1, 2, 3],
        "position": [0.1, 0.5, 0.1],
        "scale": [2.0, 2.0, 2.0],
        "rotation": [0.0, 0.0, 0.0],
        "background_id": 2,
        "camera_properties": "",
    }
    objects = []
    for object_id in sample_response["object_ids"]:
        objects.append(await get_object_from_postgres(object_id))

    sample_response["objects"] = objects
    return sample_response


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
    # TODO: get data from SQL -> convert to model

    sample_response = {
        "id": scenario_id,
        "name": "Student Escape Room",
        "friendly_name": "student-escape-room",
        "description": "A student at ABC High is going through a troubling time."
        + "They are in their Chemistry class when they realize they did not get their homework done in time."
        + " Find out what they do next in this escape room!",
        "scene_ids": [1, 2, 3],
        "is_published": False,
        "is_previewable": True,
        "publish_link": "www.publishlink.com/teacher-escape-room",
        "preview_link": "www.previewlink.com/student-escape-room",
        "expected_solve_time": "10 to 20",
    }

    return sample_response


async def delete_scenario_from_postgres(scenario_id: str):
    # TODO: delete from postgres

    sample_response = {"message": "deleted successfully"}
    return sample_response


async def update_scenario_from_postgres(scenario_id: str, data: dict):
    # TODO: update item into postgres

    sample_response = {"message": "updated scenario with id " + scenario_id}
    return sample_response  # Represents id


async def post_scene_to_postgres(data: dict):
    # TODO: insert into postgres
    return 2  # Represents id


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
