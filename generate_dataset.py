import os
import cv2
import numpy as np

INPUT_FOLDER = "data/original"

OUTPUT_FOLDERS = {
    "good": "data/good",
    "blurry": "data/blurry",
    "dark": "data/dark",
    "glare": "data/glare",
    "partial": "data/partial"
}

# Create folders
for folder in OUTPUT_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)


def add_glare(image):
    img = image.copy()

    h, w = img.shape[:2]

    center = (
        np.random.randint(w // 4, 3 * w // 4),
        np.random.randint(h // 4, 3 * h // 4)
    )

    radius = min(h, w) // 6

    overlay = img.copy()

    cv2.circle(
        overlay,
        center,
        radius,
        (255, 255, 255),
        -1
    )

    img = cv2.addWeighted(
        overlay,
        0.45,
        img,
        0.55,
        0
    )

    return img


def make_dark(image):
    return cv2.convertScaleAbs(
        image,
        alpha=0.6,
        beta=-60
    )


def make_blur(image):
    return cv2.GaussianBlur(
        image,
        (15, 15),
        0
    )


def make_partial(image):
    img = image.copy()

    h, w = img.shape[:2]

    img[:, :w // 3] = 255

    return img


count = 0

for file in os.listdir(INPUT_FOLDER):

    if not file.lower().endswith(
        (".png", ".jpg", ".jpeg")
    ):
        continue

    path = os.path.join(INPUT_FOLDER, file)

    image = cv2.imread(path)

    if image is None:
        continue

    name = os.path.splitext(file)[0]

    # Good
    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDERS["good"],
            f"{name}.png"
        ),
        image
    )

    # Blur
    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDERS["blurry"],
            f"{name}_blur.png"
        ),
        make_blur(image)
    )

    # Dark
    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDERS["dark"],
            f"{name}_dark.png"
        ),
        make_dark(image)
    )

    # Glare
    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDERS["glare"],
            f"{name}_glare.png"
        ),
        add_glare(image)
    )

    # Partial
    cv2.imwrite(
        os.path.join(
            OUTPUT_FOLDERS["partial"],
            f"{name}_partial.png"
        ),
        make_partial(image)
    )

    count += 1

print("=" * 50)
print("Dataset Generation Completed")
print("=" * 50)
print(f"Original Images : {count}")
print(f"Generated Images: {count * 5}")
print("=" * 50)