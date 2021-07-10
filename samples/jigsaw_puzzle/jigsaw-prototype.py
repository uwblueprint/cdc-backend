import base64
import io

import cv2
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
        # print(io_buffer)
        # use io_buffer as body for S3?
        # key: f"images/img{r}_{c}.png"
        # body = io_buffer
        # ContentType='image/jpeg'


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
