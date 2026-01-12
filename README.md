# 🇮🇳 Indian PCC & Passport Photo AI Studio

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A specialized AI-powered web tool designed to generate perfectly compliant digital photographs for the **Indian PCC (Police Clearance Certificate)** and **Passport** application portals. 

## 🎯 Why This Tool Exists
The Indian Government portals have extremely strict validation logic that often rejects photos due to:
1. **Dimensions:** Must be exactly **630 x 810 pixels**.
2. **File Size Floor:** Rejects files under **200 KB** (even if they are high quality).
3. **File Size Ceiling:** Must be strictly below **250 KB**.
4. **Composition:** Head height must be between 70-80% of the frame.

**This studio automates the geometry and the "digital weight" to ensure a 100% upload success rate.**

---

## ✨ Features
- **AI Face Detection:** Uses **MTCNN** to locate eyes and chin for perfect vertical alignment.
- **Precision Weighting:** Mathematically appends null-padding to hit a specific KB target (e.g., exactly 215 KB).
- **Anti-Border Logic:** Intelligent cropping that shifts the window to prevent black bars if the face is near the edge of your raw photo.
- **Side-by-Side Comparison:** Compare your original upload with the AI-processed version instantly.
- **Metadata Preservation:** Saves in high-quality JPEG format with optimized subsampling.

---

## 🚀 Installation & Local Run

### Option A: Using Docker (Recommended)
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/gulzarrf1991-boop/PCC-photo-v1.git](https://github.com/gulzarrf1991-boop/PCC-photo-v1.git)
   cd PCC-photo-v1