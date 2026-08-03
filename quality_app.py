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

st.markdown("""
<style>

/* Main Title */
.main-title{
    font-size:54px;
    font-weight:bold;
    text-align:center;
    color:#1565C0;
}

/* Subtitle */
.sub-title{
    font-size:28px;
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

/* Helper Text */
.st-emotion-cache-1v0mbdj, .st-emotion-cache-1wmy9hl, .st-emotion-cache-1kyxreq {
    font-size: 20px;
}

/* Uploader label */
.stFileUploader label, .stFileUploader p {
    font-size: 20px;
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
    color:#1565C0;
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

    # Display image
    st.image(image, channels="BGR", width=300)

    # -------------------------
    # Run all quality checks
    # -------------------------
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

    # -------------------------
    # Display Metrics
    # -------------------------
    st.header("Quality Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-name">Blur Score</div>
        <div class="metric-value">{blur['blur_score']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-name">Brightness</div>
        <div class="metric-value">{brightness['brightness']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-name">ROI Fraction</div>
        <div class="metric-value">{roi['roi_fraction']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-name">Glare Fraction</div>
        <div class="metric-value">{glare['glare_fraction']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-name">Ridge Score</div>
        <div class="metric-value">{ridge['ridge_score']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-name">Overall Score</div>
        <div class="metric-value">{score:.2f}/100</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<h2 style="text-align:center;">Overall Quality Score</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="score">{score:.2f}</div>',
        unsafe_allow_html=True
    )

    # -------------------------
    # PASS / FAIL
    # -------------------------
    if passed:
        st.markdown(
            '<div class="pass">✅ PASS</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="fail">❌ FAIL</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<p class="message">{message}</p>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section">Processing Results</p>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.image("outputs/roi_mask.png", caption="ROI Mask", use_container_width=True)

    with c2:
        st.image("outputs/gabor_output.png", caption="Gabor Filter Output", use_container_width=True)