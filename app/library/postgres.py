import uuid

import boto3
from cache.cache import update_asset_cache, update_scenario_cache, update_scene_cache
from config import config
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
    get_object_ids,
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
        raise ValueError(f"Object ID {object_id} not valid")
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

    # if the scene doesn't have a screenshot attached, attach the default
    if not response["screenshot_url"]:
        response["screenshot_url"] = (
            config.get("backend_domain") + "/static/img/scene-generic.jpeg"
        )
        response["s3_key"] = ""
    else:
        response["s3_key"] = response["screenshot_url"]
        response["screenshot_url"] = (
            config.get("asset.prefix_url") + response["screenshot_url"]
        )

    if update_cache:
        await update_scene_cache(scene_id, response)
    return response


async def get_scenes_from_postgres(session):
    scenes = get_scenes(session)
    resp_dict = {"scenes": []}
    for scene in scenes:
        # if the scene has a screenshot attached
        if scene.screenshot_url:
            scene.screenshot_url = config.get("asset.prefix_url") + scene.screenshot_url
        resp_dict["scenes"].append(scene.as_dict())

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
    asset_obj: Asset = get_asset(asset_id, session)
    if not asset_obj:
        raise ValueError("Asset ID not valid")

    scenes_resp = await get_scenes_from_postgres(session)

    for scene in scenes_resp["scenes"]:
        if asset_id == str(scene["background_id"]):
            raise AssertionError(
                f"Asset ID {asset_id} is reference as background_id in scene with ID {scene['id']}"
            )

    # only delete asset from S3 if hard delete is true
    if config.get("asset.aws_hard_delete", False):
        s3_client = boto3.client(
            "s3",
            endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
            region_name=config.get("s3.region"),
        )
        s3_client.delete_object(
            Bucket=config.get("s3.bucket_name"),
            Key=asset_obj.s3_key,
        )

        pos_key = asset_obj.screenshot_url.find("image/")

        if pos_key != -1:
            screenshot_key = asset_obj.screenshot_url[pos_key:]
            s3_client.delete_object(
                Bucket=config.get("s3.bucket_name"),
                Key=screenshot_key,
            )

    delete_asset(asset_id, session)
    object_ids = get_object_ids(session)
    for scene in scenes_resp["scenes"]:
        new_object_ids = []
        for object_id in scene["object_ids"]:
            if object_id in object_ids:
                new_object_ids.append(object_id)
        if scene["object_ids"] != new_object_ids:
            scene["object_ids"] = new_object_ids
            await update_scene_from_postgres(scene["id"], scene, session)

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
    # Get scene first
    scenario_obj: Scenario = get_scenario(scenario_id, session)
    if scenario_obj is None:
        raise ValueError("Scenario ID not valid")

    # Delete the screenshot of scenario, if it has one
    if scenario_obj.screenshot_url:
        # Only delete from AWS if config is enabled for AWS support
        if "aws" in config.get("app-env"):
            s3_client = boto3.client(
                "s3",
                endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                region_name=config.get("s3.region"),
            )
            s3_client.delete_object(
                Bucket=config.get("s3.bucket_name"),
                Key=scenario_obj.screenshot_url,
            )

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

    # Delete the screenshot of scene, if it has one
    if scene_obj.screenshot_url:
        # Only delete from AWS if config is enabled for AWS support
        if "aws" in config.get("app-env"):
            s3_client = boto3.client(
                "s3",
                endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                region_name=config.get("s3.region"),
            )
            s3_client.delete_object(
                Bucket=config.get("s3.bucket_name"),
                Key=scene_obj.screenshot_url,
            )

    # Delete the scene
    if not delete_scene(scene_id, session):
        raise ValueError("Scene ID not valid")

    # Remove the scene from scenario's scene_ids array
    scenarios = get_scenarios(session)
    for scenario in scenarios:
        for idx in range(0, len(scenario.scene_ids)):
            if int(scene_id) == scenario.scene_ids[idx]:
                del scenario.scene_ids[idx]
                del scenario.transitions[idx + 1]
                await update_scenario_from_postgres(
                    scenario.id, scenario.as_dict(), session
                )
                break

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
    # Get scene to duplicate
    curr_scene = get_scene(scene_id, session)
    if curr_scene is None:
        raise ValueError("Invalid Scene ID")
    curr_scene = curr_scene.as_dict()
    object_ids = curr_scene["object_ids"]
    curr_scene["name"] += "_copy"
    try:
        del curr_scene["id"]
        del curr_scene["object_ids"]
    except KeyError:
        pass

    # Create new duplicated scene without the objects
    new_scene = await post_scene_to_postgres(curr_scene, session)
    new_scene_id = new_scene["id"]
    new_object_ids = []
    # Duplicate the objects and get new IDs
    for object_id in object_ids:
        curr_object = get_object(object_id, session).as_dict()
        try:
            del curr_object["id"]
        except KeyError:
            pass
        object_model = Object(**curr_object)
        object_model = create_entity(object_model, session)
        new_object_ids.append(object_model.id)

    # Duplicate the screenshot, if the scene has one
    if new_scene["screenshot_url"]:
        new_screenshot_key = (
            "images/"
            + uuid.uuid4().hex
            + "."
            + new_scene["screenshot_url"].split(".")[-1]
        )
        # Only copy to AWS if config is enabled for AWS support
        if "aws" in config.get("app-env"):
            s3_client = boto3.client(
                "s3",
                endpoint_url=f"https://s3.{config.get('s3.region')}.amazonaws.com",
                region_name=config.get("s3.region"),
            )
            s3_client.copy_object(
                ACL="public-read",
                Bucket=config.get("s3.bucket_name"),
                CopySource=f"{config.get('s3.bucket_name')}/{new_scene['screenshot_url']}",
                Key=new_screenshot_key,
            )
            new_scene["screenshot_url"] = new_screenshot_key

    # Update the new scene and return
    new_scene["object_ids"] = new_object_ids
    final_scene = await update_scene_from_postgres(new_scene_id, new_scene, session)
    return final_scene


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
