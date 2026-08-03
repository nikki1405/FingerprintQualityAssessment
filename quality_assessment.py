import cv2
import numpy as np
import os


def normalize(value, min_value, max_value):
    """
    Normalize a value between 0 and 1.
    """
    value = max(min_value, min(value, max_value))
    return (value - min_value) / (max_value - min_value)


# ==========================================================
# Load Image
# ==========================================================
def load_image(image_path):
    """
    Load an image from disk.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to load image.")

    return image


# ==========================================================
# Blur Detection
# ==========================================================
def check_blur(image_bgr, threshold=10.0):
    """
    Detect image blur using Variance of Laplacian.
    """

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    blur_score = laplacian.var()

    return {
        "blur_score": round(float(blur_score), 2),
        "is_blurry": blur_score < threshold
    }

# ==========================================================
# Ridge Clarity
# ==========================================================
def check_ridge_clarity(image_bgr, roi_mask, threshold=100):
    """
    Estimate ridge clarity using a Gabor filter.
    """

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Only fingerprint region
    gray = cv2.bitwise_and(gray, gray, mask=roi_mask)

    kernel = cv2.getGaborKernel(
        (21, 21),      # Kernel size
        5.0,           # Sigma
        np.pi / 4,     # Orientation (45 degrees)
        10.0,          # Wavelength
        0.5,           # Aspect ratio
        0,
        ktype=cv2.CV_32F
    )

    filtered = cv2.filter2D(gray, cv2.CV_8UC3, kernel)

    ridge_score = filtered.var()

    return {
        "ridge_score": round(float(ridge_score), 2),
        "ridges_clear": ridge_score > threshold,
        "filtered": filtered
    }


def calculate_quality_score(
    blur_result,
    brightness_result,
    glare_result,
    roi_result,
    ridge_result
):
    """
    Calculate overall fingerprint quality score (0–100).
    """

    blur_score = normalize(blur_result["blur_score"], 10, 5000)

    brightness = brightness_result["brightness"]
    brightness_score = 1 - abs(brightness - 130) / 130
    brightness_score = max(0, min(brightness_score, 1))

    roi_score = min(roi_result["roi_fraction"] / 0.50, 1)

    glare_score = 1 - min(glare_result["glare_fraction"] / 0.05, 1)

    ridge_score = normalize(ridge_result["ridge_score"], 100, 5000)

    final_score = (
        0.25 * blur_score +
        0.20 * brightness_score +
        0.20 * roi_score +
        0.15 * glare_score +
        0.20 * ridge_score
    )

    return round(final_score * 100, 2)


# ==========================================================
# Quality Gate
# ==========================================================
def quality_gate(score):
    """
    Decide whether fingerprint passes quality check.
    """

    if score >= 80:
        return True, "Excellent Quality - Ready for Matching"

    elif score >= 60:
        return True, "Acceptable Quality - Proceed"

    else:
        return False, "Poor Quality - Please Recapture"


# ==========================================================
# Brightness Check
# ==========================================================
def check_brightness(
    image_bgr,
    dark_threshold=50,
    bright_threshold=210
):
    """
    Detect if image is too dark or too bright.
    """

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    brightness = np.mean(gray)

    return {
        "brightness": round(float(brightness), 2),
        "too_dark": brightness < dark_threshold,
        "too_bright": brightness > bright_threshold
    }


# ==========================================================
# ROI Detection
# ==========================================================
def check_roi_completeness(
    image_bgr,
    roi_threshold=0.15
):
    """
    Estimate fingerprint region.
    """

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    white_ratio = np.sum(mask == 255) / mask.size

    if white_ratio > 0.5:
        mask = cv2.bitwise_not(mask)

    finger_pixels = np.sum(mask == 255)

    total_pixels = mask.size

    roi_fraction = finger_pixels / total_pixels

    return {
        "roi_fraction": round(float(roi_fraction), 4),
        "roi_complete": roi_fraction >= roi_threshold,
        "mask": mask
    }


# ==========================================================
# Improved Glare Detection (ROI Based)
# ==========================================================
def check_glare(
    image_bgr,
    roi_mask,
    glare_threshold=240,
    max_glare_fraction=0.05
):
    """
    Detect glare only inside the fingerprint ROI.
    """

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    roi_pixels = gray[roi_mask == 255]

    if len(roi_pixels) == 0:
        return {
            "has_glare": True,
            "glare_fraction": 1.0
        }

    glare_pixels = np.sum(roi_pixels > glare_threshold)

    glare_fraction = glare_pixels / len(roi_pixels)

    return {
        "has_glare": glare_fraction > max_glare_fraction,
        "glare_fraction": round(float(glare_fraction), 4)
    }


# ==========================================================
# Main
# ==========================================================
if __name__ == "__main__":

    image_path = "data/good/sample.jpg"

    image = load_image(image_path)

    print("\n==========================================")
    print("   Fingerprint Quality Assessment System")
    print("==========================================")

    # -----------------------------------------
    # Blur
    # -----------------------------------------
    blur_result = check_blur(image)

    print("\n[1] Blur Detection")
    print("-------------------------")
    print(f"Blur Score : {blur_result['blur_score']}")

    if blur_result["is_blurry"]:
        print("Status     : ❌ Image is Blurry")
    else:
        print("Status     : ✅ Image is Sharp")

    # -----------------------------------------
    # Brightness
    # -----------------------------------------
    brightness_result = check_brightness(image)

    print("\n[2] Brightness Check")
    print("-------------------------")
    print(f"Brightness : {brightness_result['brightness']}")

    if brightness_result["too_dark"]:
        print("Status     : ❌ Too Dark")

    elif brightness_result["too_bright"]:
        print("Status     : ❌ Too Bright")

    else:
        print("Status     : ✅ Good Brightness")

    # -----------------------------------------
    # ROI
    # -----------------------------------------
    roi_result = check_roi_completeness(image)

    print("\n[3] ROI Completeness")
    print("-------------------------")
    print(f"ROI Fraction : {roi_result['roi_fraction']}")

    if roi_result["roi_complete"]:
        print("Status       : ✅ Finger Properly Captured")
    else:
        print("Status       : ❌ Finger Occupies Too Little Area")

    # Save ROI mask
    os.makedirs("outputs", exist_ok=True)
    cv2.imwrite("outputs/roi_mask.png", roi_result["mask"])

    print("\nROI mask saved to outputs/roi_mask.png")

    # -----------------------------------------
    # Glare
    # -----------------------------------------
    glare_result = check_glare(
        image,
        roi_result["mask"]
    )

    print("\n[4] Glare Detection")
    print("-------------------------")
    print(f"Glare Fraction : {glare_result['glare_fraction']}")

    if glare_result["has_glare"]:
        print("Status          : ❌ Glare Detected")
    else:
        print("Status          : ✅ No Glare")

    print("\n==========================================")
    print("Current Progress : 4 / 5 Quality Metrics")
    print("==========================================")

    # -----------------------------------------
    # Ridge Clarity
    # -----------------------------------------
    ridge_result = check_ridge_clarity(
        image,
        roi_result["mask"]
    )

    print("\n[5] Ridge Clarity")
    print("-------------------------")
    print(f"Ridge Score : {ridge_result['ridge_score']}")

    if ridge_result["ridges_clear"]:
        print("Status       : ✅ Clear Fingerprint Ridges")
    else:
        print("Status       : ❌ Poor Ridge Quality")

    cv2.imwrite(
        "outputs/gabor_output.png",
        ridge_result["filtered"]
    )

    quality_score = calculate_quality_score(
        blur_result,
        brightness_result,
        glare_result,
        roi_result,
        ridge_result
    )

    passed, message = quality_gate(quality_score)

    print("\n==========================================")
    print(" Composite Quality Assessment")
    print("==========================================")
    print(f"Overall Score : {quality_score}/100")

    if passed:
        print("Result        : ✅ PASS")
    else:
        print("Result        : ❌ FAIL")

    print(f"Message       : {message}")