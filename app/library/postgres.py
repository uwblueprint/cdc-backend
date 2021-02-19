from config import config


async def get_text_from_postgres(text_id: str):
    # TODO: get data from SQL -> convert to model

    sample_response = {
        "id": text_id,
        "next_text_id": text_id * 2,
        "content": "Hello this is what is displayed",
        "object_id": text_id * 3,
    }

    return sample_response


async def get_solved_from_postgres(object_id: str):
    # TODO: Get actual list from postgres
    next_object_ids = ["1", "2", "23", "37", object_id]
    return next_object_ids


async def post_asset_to_postgres(data: dict):
    # TODO: insert into postgres
    return 2  # Represents id


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
        "objects_id": [1, 2, 3],
        "position": [0.1, 0.5, 0.1],
        "scale": [2.0, 2.0, 2.0],
        "rotation": [0.0, 0.0, 0.0],
        "background_id": 2,
        "camera_properties": "",
    }
    objects = []
    for object_id in sample_response["objects_id"]:
        objects.append(await get_object_from_postgres(object_id))

    sample_response["objects"] = objects
    return sample_response


async def get_asset_from_postgres(asset_id: str):
    # TODO: get data from SQL -> convert to model

    sample_response = {
        "id": asset_id,
        "name": "cup",
        "s3_key": "cup.file",
        "obj_type": config.get("asset.allowed_asset_types")[1],
    }

    return sample_response


async def delete_asset_from_postgres(asset_id: str):
    # TODO: delete from postgres

    sample_response = {"message": "deleted successfully"}

    return sample_response
