# 🖐 Contactless Fingerprint Quality Assessment System

## 📌 Overview

The **Contactless Fingerprint Quality Assessment System** is a computer vision-based application developed using **Python, OpenCV, NumPy, Pandas, and Streamlit**. The system evaluates the quality of contactless fingerprint images before they are used for biometric authentication.

It automatically detects various quality issues such as:

- Blur
- Poor Brightness
- Incomplete Fingerprint Region (ROI)
- Glare
- Poor Ridge Clarity

Based on these metrics, the system computes an **Overall Quality Score (0–100)** and classifies the fingerprint as **PASS** or **FAIL**.

---

## 🎯 Objectives

- Evaluate contactless fingerprint image quality.
- Detect blurred fingerprint images.
- Measure brightness and exposure.
- Estimate fingerprint ROI completeness.
- Detect glare within the fingerprint region.
- Analyze ridge clarity using Gabor filters.
- Compute a composite fingerprint quality score.
- Provide an interactive Streamlit web application.
- Support batch testing on multiple fingerprint images.

---

# ✨ Features

- 📤 Upload fingerprint images
- 🔍 Blur Detection
- 💡 Brightness Analysis
- ✋ ROI Completeness Detection
- ☀️ Glare Detection
- 🌊 Ridge Clarity Analysis
- 📊 Composite Quality Score
- ✅ PASS / FAIL Decision
- 🎨 ROI Mask Visualization
- 🎯 Gabor Filter Output
- 📁 Batch Dataset Testing
- 📄 CSV Result Generation

---

# 🛠 Technologies Used

| Technology | Purpose                 |
| ---------- | ----------------------- |
| Python     | Programming Language    |
| OpenCV     | Image Processing        |
| NumPy      | Numerical Computing     |
| Pandas     | CSV Handling            |
| Streamlit  | Web Application         |
| VS Code    | Development Environment |

---

# 🧠 Algorithms Used

## 1. Blur Detection

**Algorithm:** Variance of Laplacian

Purpose:

- Detects whether the fingerprint image is blurred.

Output:

- Blur Score
- Sharp / Blurry Decision

---

## 2. Brightness Analysis

**Algorithm:** Mean Grayscale Intensity

Purpose:

- Detects underexposed and overexposed images.

Output:

- Brightness Value
- Good / Dark / Bright

---

## 3. ROI Detection

**Algorithm:** Otsu Thresholding

Purpose:

- Extracts the fingerprint region.
- Measures fingerprint coverage.

Output:

- ROI Fraction
- ROI Mask

---

## 4. Glare Detection

Purpose:

- Detects bright reflection regions.
- Calculates glare fraction inside ROI.

Output:

- Glare Fraction
- Glare Status

---

## 5. Ridge Clarity

**Algorithm:** Gabor Filtering

Purpose:

- Enhances fingerprint ridges.
- Measures ridge visibility.

Output:

- Ridge Score
- Ridge Enhanced Image

---

## 6. Composite Quality Score

The final quality score is calculated using:

- Blur
- Brightness
- ROI
- Glare
- Ridge Clarity

Final Score:

```
0 – 100
```

Decision:

- PASS
- FAIL

---

# 📂 Project Structure

```
FingerprintQualityAssessment/
│
├── data/
│   ├── original/
│   ├── good/
│   ├── blurry/
│   ├── dark/
│   ├── glare/
│   └── partial/
│
├── outputs/
│   ├── roi_mask.png
│   └── gabor_output.png
│
├── screenshots/
│
├── quality_assessment.py
├── quality_app.py
├── generate_dataset.py
├── test_quality.py
├── results.csv
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/FingerprintQualityAssessment.git
```

Move into the project

```bash
cd FingerprintQualityAssessment
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the Streamlit application

```bash
streamlit run quality_app.py
```

Open the URL displayed in the terminal.

---

# 📁 Dataset Generation

Place original fingerprint images inside

```
data/original/
```

Generate the testing dataset

```bash
python generate_dataset.py
```

Generated folders

```
good/
blurry/
dark/
glare/
partial/
```

---

# 📊 Batch Testing

Run

```bash
python test_quality.py
```

Output

```
results.csv
```

---

# 📈 Sample Results

| Category | Average Result                           |
| -------- | ---------------------------------------- |
| Good     | PASS                                     |
| Blurry   | Mostly FAIL                              |
| Dark     | Acceptable / FAIL (depends on threshold) |
| Glare    | Evaluated using glare detection          |
| Partial  | FAIL                                     |

---

# 📊 Quality Metrics

The application evaluates the following metrics:

- Blur Score
- Brightness
- ROI Fraction
- Glare Fraction
- Ridge Score
- Overall Quality Score

# 📚 References

1. OpenCV Documentation
2. Streamlit Documentation
3. Fingerprint Verification Competition (FVC) Datasets
4. Gabor Filter-based Fingerprint Enhancement Research Papers

---
