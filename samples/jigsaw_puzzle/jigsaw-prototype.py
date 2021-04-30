import cv2

# TODO: Add opencv-python to requirements

img = cv2.imread("images/whmis_labels.jpg")
rows = 3
cols = 3
pixelXscale = int(img.shape[0] / rows)
pixelYscale = int(img.shape[1] / cols)

for r in range(1, rows + 1):
    for c in range(1, cols + 1):
        cv2.imwrite(
            f"images/img{r}_{c}.png",
            img[
                (r - 1) * pixelXscale : r * pixelXscale,  # noqa: E203
                (c - 1) * pixelYscale : c * pixelYscale,  # noqa: E203
            ],
        )
