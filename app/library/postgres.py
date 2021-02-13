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
