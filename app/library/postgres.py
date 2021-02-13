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
