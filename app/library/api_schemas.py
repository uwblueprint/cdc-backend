from config import config

# Schemas for the various endpoints

admin_asset_post_handler_schema = {
    "type": "object",
    "properties": {
        "display_name": {"type": "string", "pattern": "^[a-zA-Z _-]{,50}$"},
        "object_type": {
            "enum": config.get("asset.allowed_asset_types"),
        },
    },
    "required": ["display_name", "object_type"],
}
