from config import config

# Schemas for the various endpoints

admin_asset_handler_body_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{1,50}$"},
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
        "name": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{1,50}$"},
        "friendly_name": {"type": "string", "pattern": r"^[a-zA-Z0-9_-]{1,50}$"},
        "description": {
            "type": "string",
            "pattern": r"^[\?\!\.,a-zA-Z0-9 _-]{,2000}$",
        },
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
        "name": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{1,50}$"},
        "friendly_name": {"type": "string", "pattern": r"^[a-zA-Z0-9_-]{1,50}$"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z0-9 _-]{,2000}$"},
        "scene_ids": {"type": "array", "items": {"type": "integer"}},
        "is_published": {"type": "boolean"},
        "is_previewable": {"type": "boolean"},
        "publish_link": {"type": "string", "pattern": r"^[\S]{1,50}$"},
        "preview_link": {"type": "string", "pattern": r"^[\S]{1,50}$"},
        "expected_solve_time": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{,50}$"},
        "introduction_data": {
            "type": "object",
            "properties": {
                "header_text": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "conclusion_data": {
            "type": "object",
            "properties": {
                "header_text": {"type": "string"},
                "paragraph_text": {"type": "string"},
                "share_link": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "transitions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "imageSrc": {"type": "string"},
                            },
                            "required": ["text"],
                            "additionalProperties": False,
                        },
                    },
                    "currPosition": {"type": "integer"},
                },
                "required": ["data", "currPosition"],
                "additionalProperties": False,
            },
        },
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
        "name": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{1,50}$"},
        "background_id": {"type": "integer"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z0-9 _-]{,2000}$"},
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
        "name": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{1,50}$"},
        "description": {"type": "string", "pattern": r"^[\?\!\.,a-zA-Z0-9 _-]{,2000}$"},
        "object_ids": {"type": "array", "items": {"type": "integer"}},
        "position": {"type": "array", "items": {"type": "number"}},
        "scale": {"type": "array", "items": {"type": "number"}},
        "rotation": {"type": "array", "items": {"type": "number"}},
        "background_id": {"type": "integer"},
        "hints": {
            "type": "array",
            "items": {"type": "string", "pattern": r"^[\:\?\!\.,a-zA-Z0-9 _-]{1,200}$"},
        },
        "camera_properties": {
            "type": "object",
            "properties": {
                "position": {"type": "array", "items": {"type": "number"}},
                "look_controls": {"type": "boolean"},
                "wasd_controls": {"type": "boolean"},
                "cursor_properties": {
                    "type": "object",
                    "properties": {
                        "asset_id": {"type": "integer"},
                        "shape": {"type": "string", "pattern": r"^[a-zA-Z _-]{1,20}$"},
                        "position": {"type": "array", "items": {"type": "number"}},
                    },
                    "required": [
                        "position",
                    ],
                },
            },
            "required": ["look_controls", "position", "wasd_controls"],
        },
    },
    "required": [
        "name",
        "description",
        "position",
        "scale",
        "rotation",
        "background_id",
        "camera_properties",
    ],
    "additionalProperties": False,
}

admin_object_handler_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-zA-Z0-9 _-]{1,50}$"},
        "position": {"type": "array", "items": {"type": "number"}},
        "scale": {"type": "array", "items": {"type": "number"}},
        "rotation": {"type": "array", "items": {"type": "number"}},
        "asset_id": {"type": "integer"},
        "next_objects": {"type": "array", "items": {"type": "object"}},
        "texts": {
            "type": "array",
            "items": {"type": "string", "pattern": r"^[\S\s]{0,2000}$"},
        },
        "is_interactable": {"type": "boolean"},
        # TODO: validate animations_json once frontend is more developed
        "animations_json": {"type": "object"},
    },
    "required": [
        "name",
        "position",
        "scale",
        "rotation",
        "asset_id",
        "next_objects",
        "is_interactable",
    ],
    "additionalProperties": False,
}

admin_aws_handler_body_schema = {
    "type": "object",
    "properties": {
        "type": {
            "enum": config.get("s3.allowed_types"),
        },
        "extension": {
            "enum": config.get("s3.allowed_extensions"),
        },
        "s3_key": {"type": "string"},
    },
    "required": ["type"],
    "additionalProperties": False,
}
