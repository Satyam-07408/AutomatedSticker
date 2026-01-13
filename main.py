import cv2
import numpy as np
import os

# =============================
# CONFIGURATION
# =============================
DATASET_DIR = "dataset"
OUTPUT_DIR = "outputs"

STICKER_OFFSET = 30        # distance from box edge
STICKER_WIDTH = 40         # sticker width (pixels)
STICKER_HEIGHT = 20        # sticker height (pixels)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================
# PROCESS EACH IMAGE
# =============================
for image_name in os.listdir(DATASET_DIR):

    if not image_name.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    image_path = os.path.join(DATASET_DIR, image_name)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read {image_name}")
        continue

    # -----------------------------
    # PREPROCESSING
    # -----------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # -----------------------------
    # CONTOUR DETECTION
    # -----------------------------
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:
        print(f"No contours found in {image_name}")
        continue

    box_contour = max(contours, key=cv2.contourArea)

    # -----------------------------
    # ORIENTATION ESTIMATION
    # -----------------------------
    rect = cv2.minAreaRect(box_contour)
    (cx, cy), (w, h), angle = rect

    if w < h:
        angle += 90

    # Box contour (for visualization)
    box = cv2.boxPoints(rect)
    box = np.int32(box)

    # -----------------------------
    # FIXED STICKER PLACEMENT (BOX FRAME)
    # -----------------------------
    theta = np.deg2rad(angle)

    dx = w / 2 - STICKER_OFFSET
    dy = -h / 2 + STICKER_OFFSET

    rot_x = dx * np.cos(theta) - dy * np.sin(theta)
    rot_y = dx * np.sin(theta) + dy * np.cos(theta)

    sticker_x = int(cx + rot_x)
    sticker_y = int(cy + rot_y)

    # DEBUG: visualize box-frame vector (center → sticker)
    cv2.line(
        image,
        (int(cx), int(cy)),
        (sticker_x, sticker_y),
        (0, 0, 255),
        1
    )

    # -----------------------------
    # DRAW STICKER AS ROTATED RECTANGLE
    # -----------------------------
    sticker_rect = (
        (sticker_x, sticker_y),
        (STICKER_WIDTH, STICKER_HEIGHT),
        angle
    )

    sticker_box = cv2.boxPoints(sticker_rect)
    sticker_box = np.int32(sticker_box)

    cv2.drawContours(image, [sticker_box], 0, (0, 0, 255), -1)

    # -----------------------------
    # VISUALIZATION
    # -----------------------------
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

    # Orientation axis
    axis_length = 100
    x2 = int(cx + axis_length * np.cos(theta))
    y2 = int(cy + axis_length * np.sin(theta))
    cv2.line(
        image,
        (int(cx), int(cy)),
        (x2, y2),
        (255, 0, 0),
        2
    )

    # -----------------------------
    # SAVE OUTPUT
    # -----------------------------
    output_path = os.path.join(OUTPUT_DIR, f"result_{image_name}")
    cv2.imwrite(output_path, image)

    # -----------------------------
    # PRINT RESULTS
    # -----------------------------
    print("===================================")
    print(f"Image: {image_name}")
    print(f"Orientation angle (deg): {round(angle, 2)}")
    print(f"Sticker position (x, y): ({sticker_x}, {sticker_y})")

print("\nProcessing complete. Results saved in 'outputs/' folder.")
