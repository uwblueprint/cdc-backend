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


async def update_asset_from_postgres(asset_id: str, data: dict):
    # TODO: update item into postgres

    sample_response = {"message": "updated asset with id " + asset_id}
    return sample_response  # Represents id


async def post_scenario_to_postgres(data: dict):
    # TODO: insert into postgres
    return 2  # Represents id


async def get_scenario_from_postgres(asset_id: str):
    # TODO: get data from SQL -> convert to model

    sample_response = {
        "id": asset_id,
        "name": "Student Escape Room",
        "friendly_name": "student-escape-room",
        "description": "A student at ABC High is going through a troubling time."
        + "They are in their Chemistry class when they realize they did not get their homework done in time."
        + " Find out what they do next in this escape room!",
        "scene_ids": [1, 2, 3],
        "is_published": False,
        "is_previewable": True,
        "preview_link": "www.previewlink.com/student-escape-room",
        "expected_solve_time": "10 to 20",
    }

    return sample_response


async def delete_scenario_from_postgres(asset_id: str):
    # TODO: delete from postgres

    sample_response = {"message": "deleted successfully"}

    return sample_response


async def update_scenario_from_postgres(asset_id: str, data: dict):
    # TODO: update item into postgres

    sample_response = {"message": "updated scenario with id " + asset_id}
    return sample_response  # Represents id
