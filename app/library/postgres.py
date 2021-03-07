from models.asset import Asset
from models.db_client import (  # delete_text,
    create_entity,
    delete_asset,
    delete_object,
    delete_scenario,
    delete_scene,
    get_asset,
    get_object,
    get_scenario,
    get_scene,
    get_text,
    put_asset,
    put_object,
    put_scenario,
    put_scene,
    put_text,
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
    if not delete_asset(asset_id):
        raise ValueError("Asset ID not valid")

    response = {"message": "Deleted successfully"}
    return response


async def update_asset_from_postgres(asset_id: str, data: dict):
    num_assets_updated = put_asset(asset_id, data)
    if num_assets_updated == 0:
        raise ValueError("Invalid Asset ID")
    return await get_asset_from_postgres(asset_id)


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
    if not delete_scenario(scenario_id):
        raise ValueError("Scenario ID not valid")

    response = {"message": "Deleted successfully"}
    return response


async def update_scenario_from_postgres(scenario_id: str, data: dict):
    num_scenarios_updated = put_scenario(scenario_id, data)
    if num_scenarios_updated == 0:
        raise ValueError("Invalid Scenario ID")
    return await get_scenario_from_postgres(scenario_id)


async def post_scene_to_postgres(data: dict):
    scene_model = Scene(**data)
    scene_model = create_entity(scene_model)
    return scene_model.as_dict()


async def update_scene_from_postgres(scene_id: str, data: dict):
    num_scenes_updated = put_scene(scene_id, data)
    if num_scenes_updated == 0:
        raise ValueError("Invalid scene ID")
    return await get_scene_from_postgres(scene_id)


async def delete_scene_from_postgres(scene_id: str):
    # Get scene first
    scene_obj: Scene = get_scene(scene_id)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    # Delete all objects in the scene
    for object_id in scene_obj.object_ids:
        await delete_object_in_postgres(scene_id, object_id)

    # Delete the scene
    if not delete_scene(scene_id):
        raise ValueError("Scene ID not valid")

    response = {"message": "Deleted successfully"}
    return response


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

    # Ensure each object exists and it is either an object, as postgres won't do validation for us
    for next_obj in object_model.next_objects:
        try:
            await get_object_from_postgres(next_obj["id"])
        except KeyError:
            raise ValueError("one of the objects in next_objects is missing id")
        except ValueError:
            raise ValueError(
                "one of the objects in next_objects refers to an invalid id"
            )

    # Make sure the scene exists
    scene_obj: Scene = get_scene(scene_id)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    object_model = create_entity(object_model)

    # Add object to the scene
    scene_obj.object_ids.append(object_model.id)
    put_scene(scene_id, scene_obj.as_dict())

    return object_model.as_dict()


async def update_object_in_postgres(scene_id: str, object_id: str, data: dict):
    num_objects_updated = put_object(object_id, data)
    if num_objects_updated == 0:
        raise ValueError("Invalid Object ID")

    return await get_object_from_postgres(object_id)


async def delete_object_in_postgres(scene_id: str, object_id: str):
    # Make sure the scene exists
    scene_obj: Scene = get_scene(scene_id)
    if scene_obj is None:
        raise ValueError("Invalid Scene ID")

    object_model = await get_object_from_postgres(object_id)

    if not delete_object(object_id):
        raise ValueError("Object ID not valid")

    # Remove object from the scene
    if int(object_id) in scene_obj.object_ids:
        scene_obj.object_ids.remove(int(object_id))
        put_scene(scene_id, scene_obj.as_dict())

    # Delete any texts associated with the object
    if object_model["text_id"]:
        await delete_text_from_postgres(scene_id, object_model["text_id"])

    response = {"message": "Deleted successfully"}
    return response


async def post_text_to_postgres(scene_id: str, data: dict):
    text_obj = Text(**data)
    text_obj = create_entity(text_obj)

    return text_obj.as_dict()


async def put_text_to_postgres(scene_id: str, text_id: str, data: dict):
    num_texts_updated = put_text(text_id, data)
    if num_texts_updated == 0:
        raise ValueError("Invalid Text ID")

    return await get_text_from_postgres(text_id)


async def delete_text_from_postgres(
    scene_id: str, text_id: str, obj_model: Object = None
):
    # # ensure that it exists
    # text_obj: Text = get_text(text_id)
    # if text_obj is None:
    #     raise ValueError("Invalid Text ID")
    #
    # # Remove reference from object if it exists and references this text
    # if not obj_model:
    #     obj_model = get_object(text_obj.object_id)
    #
    # if obj_model and obj_model.text_id == int(text_id):
    #     obj_model.text_id = None
    #     put_object(obj_model.id, obj_model.as_dict())
    #
    # if not delete_text(text_id):
    #     raise ValueError("Text ID not valid")
    #
    # # Recursively delete the next texts in the list
    # if text_obj.next_text_id:
    #     await delete_text_from_postgres(scene_id, str(text_obj.next_text_id), obj_model)

    # TODO: this will most likely need more discussion and schema changes
    response = {"message": "Deleted successfully"}
    return response
