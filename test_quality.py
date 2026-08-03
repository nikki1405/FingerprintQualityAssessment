import os
import pandas as pd

from quality_assessment import (
    load_image,
    check_blur,
    check_brightness,
    check_roi_completeness,
    check_glare,
    check_ridge_clarity,
    calculate_quality_score,
    quality_gate
)

# -----------------------------------------
# Dataset folders
# -----------------------------------------
DATASET_FOLDERS = [
    "data/good",
    "data/blurry",
    "data/dark",
    "data/glare"
]

results = []

# -----------------------------------------
# Process each folder
# -----------------------------------------
for folder in DATASET_FOLDERS:

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        continue

    print(f"\nProcessing: {folder}")

    for file in os.listdir(folder):

        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        image_path = os.path.join(folder, file)

        try:

            image = load_image(image_path)

            blur = check_blur(image)

            brightness = check_brightness(image)

            roi = check_roi_completeness(image)

            glare = check_glare(image, roi["mask"])

            ridge = check_ridge_clarity(image, roi["mask"])

            score = calculate_quality_score(
                blur,
                brightness,
                glare,
                roi,
                ridge
            )

            passed, message = quality_gate(score)

            results.append({

                "Image": file,

                "Category": os.path.basename(folder),

                "Blur Score": blur["blur_score"],

                "Brightness": brightness["brightness"],

                "ROI Fraction": roi["roi_fraction"],

                "Glare Fraction": glare["glare_fraction"],

                "Ridge Score": ridge["ridge_score"],

                "Overall Score": score,

                "Result": "PASS" if passed else "FAIL",

                "Message": message

            })

            print(f"✓ {file}  --> {score:.2f}")

        except Exception as e:

            print(f"Error processing {file}")

            print(e)

# -----------------------------------------
# Save CSV
# -----------------------------------------
df = pd.DataFrame(results)

df.to_csv("results.csv", index=False)

print("\n=========================================")
print("Batch Testing Completed")
print("=========================================")
print(df)

print("\nResults saved to results.csv")