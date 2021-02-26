from config import config

# Schemas for the various endpoints

admin_asset_handler_body_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "obj_type": {
            "enum": config.get("asset.allowed_asset_types"),
        },
        "s3_key": {"type": "string", "pattern": r"^[\S]{1,50}$"},
    },
    "required": ["name", "obj_type", "s3_key"],
    "additionalProperties": False,
}

admin_scenario_post_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "friendly_name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z _-]{,2000}$"},
    },
    "required": [
        "name",
        "friendly_name",
        "description",
    ],
    "additionalProperties": False,
}

admin_scenario_put_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "friendly_name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z _-]{,2000}$"},
        "scene_ids": {"type": "array"},
        "is_published": {"type": "boolean"},
        "is_previewable": {"type": "boolean"},
        "publish_link": {"type": "string", "pattern": r"^[\S]{1,50}$"},
        "preview_link": {"type": "string", "pattern": r"^[\S]{1,50}$"},
        "expected_solve_time": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{,50}$"},
    },
    "required": [
        "name",
        "friendly_name",
        "description",
        "scene_ids",
        "is_published",
        "is_previewable",
    ],
    "additionalProperties": False,
}

admin_scene_post_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "background_id": {"type": "integer"},
    },
    "required": [
        "name",
        "background_id",
    ],
    "additionalProperties": False,
}

admin_scene_put_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z _-]{,2000}$"},
        "object_ids": {"type": "array"},
        "position": {"type": "array"},
        "scale": {"type": "array"},
        "rotation": {"type": "array"},
        "background_id": {"type": "integer"},
    },
    "required": [
        "name",
        "description",
        "object_ids",
        "position",
        "scale",
        "rotation",
        "background_id",
    ],
    "additionalProperties": False,
}

admin_object_handler_schema = {
    "type": "object",
    "properties": {
        "position": {"type": "array", "items": {"type": "number"}},
        "scale": {"type": "array", "items": {"type": "number"}},
        "rotation": {"type": "array", "items": {"type": "number"}},
        "asset_id": {"type": "integer"},
        "next_objects": {"type": "array"},
        "text_id": {"type": "integer"},
        "is_interactable": {"type": "boolean"},
        "animations_json": {"type": "object"},
    },
    "required": [
        "position",
        "scale",
        "rotation",
        "asset_id",
        "next_objects",
        "text_id",
        "is_interactable",
        "animations_json",
    ],
    "additionalProperties": False,
}


admin_text_handler_schema = {
    "type": "object",
    "properties": {
        "content": {"type": "string"},
        "object_id": {"type": "integer"},
        "next_text_id": {"type": "integer"},
    },
    "required": ["content", "object_id"],
    "additionalProperties": False,
}
