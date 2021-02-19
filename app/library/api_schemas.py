from config import config

# Schemas for the various endpoints

admin_asset_handler_body_schema = {
    "type": "object",
    "properties": {
        "display_name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "object_type": {
            "enum": config.get("asset.allowed_asset_types"),
        },
        "s3_prefix": {"type": "string", "pattern": r"^[\S]{1,50}$"},
    },
    "required": ["display_name", "object_type", "s3_prefix"],
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
}

admin_scene_post_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "background_id": {"type": "integer", "pattern": r"^[0-9]{1,16}$"},
    },
    "required": [
        "name",
        "background_id",
    ],
}

admin_scene_put_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z _-]{,50}$"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z _-]{,2000}$"},
        "objects_id": {"type": "array"},
        "position": {"type": "array"},
        "scale": {"type": "array"},
        "rotation": {"type": "array"},
        "background_id": {"type": "integer", "pattern": r"^[0-9]{1,16}$"},
    },
    "required": [
        "name",
        "description",
        "objects_id",
        "position",
        "scale",
        "rotation",
        "background_id",
    ],
}
