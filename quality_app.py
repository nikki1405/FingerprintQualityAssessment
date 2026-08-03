import os
import streamlit as st

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

st.set_page_config(
    page_title="Fingerprint Quality Assessment",
    page_icon="🖐",
    layout="wide"
)

# =========================================================
# SIDEBAR CONTROLS
# =========================================================
st.sidebar.title("⚙️ Quality Parameters")

blur_threshold = st.sidebar.slider(
    "Blur Threshold",
    1,
    100,
    10
)

dark_threshold = st.sidebar.slider(
    "Minimum Brightness",
    0,
    120,
    50
)

bright_threshold = st.sidebar.slider(
    "Maximum Brightness",
    150,
    255,
    210
)

roi_threshold = st.sidebar.slider(
    "ROI Threshold",
    0.0,
    1.0,
    0.15
)

glare_threshold = st.sidebar.slider(
    "Glare Fraction",
    0.00,
    0.20,
    0.05
)

# =========================================================
# STYLING
# =========================================================
st.markdown("""
<style>

/* Main Title */
.main-title{
    font-size:64px;
    font-weight:bold;
    text-align:center;
    color:#1565C0;
    line-height:1.2;
}

/* Subtitle */
.sub-title{
    font-size:32px;
    text-align:center;
    color:gray;
    margin-bottom:24px;
    line-height:1.3;
}

/* Helper Text */
.st-emotion-cache-1v0mbdj, .st-emotion-cache-1wmy9hl, .st-emotion-cache-1kyxreq,
[data-testid="stFileUploader"], [data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
.stMarkdown {
    font-size: 24px;
    line-height: 1.4;
}

/* Uploader label */
.stFileUploader label, .stFileUploader p {
    font-size: 24px;
}

/* Section Header */
.section{
    font-size:30px;
    font-weight:bold;
    color:#0D47A1;
}

/* Metric Card */
.metric-card{
    background:#F5F7FA;
    border-radius:15px;
    padding:18px;
    text-align:center;
    margin-bottom:15px;
    box-shadow:2px 2px 8px rgba(0,0,0,0.15);
}

.metric-name{
    font-size:22px;
    font-weight:bold;
    color:#333;
}

.metric-value{
    font-size:34px;
    font-weight:bold;
}

/* PASS */
.pass{
    background:#4CAF50;
    color:white;
    font-size:34px;
    font-weight:bold;
    padding:18px;
    border-radius:15px;
    text-align:center;
}

/* FAIL */
.fail{
    background:#F44336;
    color:white;
    font-size:34px;
    font-weight:bold;
    padding:18px;
    border-radius:15px;
    text-align:center;
}

/* Overall Score */
.score{
    font-size:60px;
    color:#1565C0;
    font-weight:bold;
    text-align:center;
}

/* Message */
.message{
    font-size:24px;
    text-align:center;
    font-weight:bold;
    color:#333;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">🖐 Fingerprint Quality Assessment System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">AI Based Contactless Fingerprint Image Quality Evaluation</p>',
    unsafe_allow_html=True
)

st.write(
    "Upload a contactless fingerprint image to evaluate its quality."
)


# =========================================================
# HELPER: Color coding for metric cards
# =========================================================
def get_color(value, low, high):
    """Return red/orange/green depending on where value falls."""
    if value < low:
        return "#F44336"
    elif value < high:
        return "#FF9800"
    return "#4CAF50"


def metric_card(name, value, color):
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-name">{name}</div>
    <div class="metric-value" style="color:{color};">{value}</div>
    </div>
    """, unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    "Choose a fingerprint image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Create temp folder
    os.makedirs("temp", exist_ok=True)

    image_path = os.path.join("temp", uploaded_file.name)

    # Save uploaded file
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load image
    image = load_image(image_path)

    # -------------------------
    # Run all quality checks (using sidebar thresholds)
    # -------------------------
    blur = check_blur(image, blur_threshold)

    brightness = check_brightness(
        image,
        dark_threshold,
        bright_threshold
    )

    roi = check_roi_completeness(image, roi_threshold)

    glare = check_glare(
        image,
        roi["mask"],
        max_glare_fraction=glare_threshold
    )

    ridge = check_ridge_clarity(image, roi["mask"])

    score = calculate_quality_score(
        blur,
        brightness,
        glare,
        roi,
        ridge
    )

    passed, message = quality_gate(score)

    # -------------------------
    # Three Column Dashboard Layout
    # -------------------------
    left, middle, right = st.columns([1.3, 1.2, 1])

    with left:
        st.subheader("Uploaded Fingerprint")
        st.image(
            image,
            channels="BGR",
            use_container_width=True
        )

    with middle:
        st.subheader("Quality Metrics")

        blur_color = get_color(blur["blur_score"], 100, 1000)
        brightness_color = get_color(brightness["brightness"], dark_threshold, bright_threshold)
        roi_color = get_color(roi["roi_fraction"], 0.5, 0.8)
        glare_color = get_color(1 - glare["glare_fraction"], 0.85, 0.95)
        ridge_color = get_color(ridge["ridge_score"], 50, 80)

        metric_card("Blur Score", f"{blur['blur_score']:.2f}", blur_color)
        metric_card("Brightness", f"{brightness['brightness']:.2f}", brightness_color)
        metric_card("ROI Fraction", f"{roi['roi_fraction']:.2f}", roi_color)
        metric_card("Glare Fraction", f"{glare['glare_fraction']:.4f}", glare_color)
        metric_card("Ridge Score", f"{ridge['ridge_score']:.2f}", ridge_color)

    with right:
        st.subheader("Quality Assessment")

        st.markdown(
            f'<div class="score">{score:.2f}/100</div>',
            unsafe_allow_html=True
        )

        # Gauge-style stars
        stars = int(score // 10)
        st.markdown(
            f"<h1 style='text-align:center;color:#FFB300;'>{'⭐' * stars}{'☆' * (10 - stars)}</h1>",
            unsafe_allow_html=True
        )

        st.progress(min(max(score / 100, 0.0), 1.0))
        st.caption(f"Quality Score : {score:.2f}%")

        if passed:
            st.success("✅ PASS")
        else:
            st.error("❌ FAIL")

        st.info(message)

        # -------------------------
        # Download Report Button
        # -------------------------
        report = f"""Fingerprint Quality Report
---------------------------
Blur Score     : {blur['blur_score']:.2f}
Brightness     : {brightness['brightness']:.2f}
ROI Fraction   : {roi['roi_fraction']:.2f}
Glare Fraction : {glare['glare_fraction']:.4f}
Ridge Score    : {ridge['ridge_score']:.2f}

Overall Score  : {score:.2f}/100
Result         : {"PASS" if passed else "FAIL"}
Message        : {message}
"""

        st.download_button(
            "📄 Download Report",
            report,
            file_name="quality_report.txt"
        )

    # -------------------------
    # Processing Results (ROI Mask + Gabor Output)
    # -------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section">Processing Results</p>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.image("outputs/roi_mask.png", caption="ROI Mask", width="stretch")

    with c2:
        st.image("outputs/gabor_output.png", caption="Gabor Filter Output", width="stretch")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    """
    <center>

    Developed for Assignment 4

    Contactless Fingerprint Quality Assessment

    OpenCV • Streamlit • Python

    </center>
    """,
    unsafe_allow_html=True
)