with asset_json (doc) as (
   values
    ('[
          {
            "name": "Teacup",
            "obj_type": "object",
            "s3_key": "aws_s3_route"
          },
          {
            "name": "Playground",
            "obj_type": "background",
            "s3_key": "aws_s3_route"
          },
          {
            "name": "Textbook",
            "obj_type": "object",
            "s3_key": "aws_s3_route"
          },
          {
            "name": "Seashell",
            "obj_type": "object",
            "s3_key": "aws_s3_route"
          },
          {
            "name": "Bedroom",
            "obj_type": "background",
            "s3_key": "aws_s3_route"
          }
    ]'::json)
)
insert into asset (name, s3_key, obj_type)
select name, s3_key, obj_type
from asset_json l
  cross join lateral json_populate_recordset(null::asset, doc)