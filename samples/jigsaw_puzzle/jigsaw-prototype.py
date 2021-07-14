import base64
import io
import uuid

import boto3
import cv2
from botocore.config import Config
from numpy import frombuffer, uint8

f = open("b64/lightOn", "r")
string_data = f.read()

nparr = frombuffer(base64.b64decode(string_data), uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

f.close()
rows = 3
cols = 3
pixelXscale = int(img.shape[0] / rows)
pixelYscale = int(img.shape[1] / cols)

s3_client = boto3.client(
    "s3",
    config=Config(signature_version="s3v4"),
    endpoint_url="https://s3.us-east-2.amazonaws.com",
    region_name="us-east-2",
)

s3_key_prefix = "jay/images/" + uuid.uuid4().hex + "-"
s3_key_counter = 0

for r in range(1, rows + 1):
    for c in range(1, cols + 1):
        _, buffer = cv2.imencode(
            ".png",
            img[
                (r - 1) * pixelXscale : r * pixelXscale,  # noqa: E203
                (c - 1) * pixelYscale : c * pixelYscale,  # noqa: E203
            ],
        )
        io_buffer = io.BytesIO(buffer)
        s3_client.upload_fileobj(
            Fileobj=io_buffer,
            Bucket="dcc-bp-public-dev",
            Key=s3_key_prefix + str(s3_key_counter) + ".png",
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"},
        )
        s3_key_counter += 1


# old code, saved for reference
# for r in range(1, rows + 1):
#     for c in range(1, cols + 1):
#         cv2.imwrite(
#             f"images/img{r}_{c}.png",
#             img[
#                 (r - 1) * pixelXscale : r * pixelXscale,  # noqa: E203
#                 (c - 1) * pixelYscale : c * pixelYscale,  # noqa: E203
#             ],
#         )
