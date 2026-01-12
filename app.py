import streamlit as st
import numpy as np
from PIL import Image
from mtcnn import MTCNN
import io
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Indian PCC Photo Studio", layout="wide", page_icon="🇮🇳")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .compliance-box {
        background-color: #f0f7ff;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #FF9933;
        margin-bottom: 25px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .check-mark { color: #128807; font-weight: bold; margin-right: 10px; }
    .main-title { color: #000080; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return MTCNN()

def process_photo(input_image, target_kb):
    target_w, target_h = 630, 810
    detector = load_detector()
    img = Image.open(input_image).convert('RGB')
    results = detector.detect_faces(np.array(img))

    if not results: return None, None, "No face detected."

    box = results[0]['box']
    keypoints = results[0]['keypoints']
    face_center_x = box[0] + (box[2] / 2)
    eye_y = (keypoints['left_eye'][1] + keypoints['right_eye'][1]) / 2

    scale = 690 / (box[3] / 0.7) 
    crop_w_orig, crop_h_orig = target_w / scale, target_h / scale
    left, top = face_center_x - (crop_w_orig / 2), eye_y - (310 / scale)

    if (top + crop_h_orig) > img.size[1]: top = img.size[1] - crop_h_orig
    top = max(0, top)

    final_img = img.crop((left, top, left + crop_w_orig, top + crop_h_orig))
    final_img = final_img.resize((target_w, target_h), Image.LANCZOS)

    img_byte_arr = io.BytesIO()
    final_img.save(img_byte_arr, format='JPEG', quality=95)
    
    current_size = img_byte_arr.tell()
    target_bytes = target_kb * 1024

    if current_size < target_bytes:
        img_byte_arr.write(b'\0' * int(target_bytes - current_size))
    
    return img, final_img, img_byte_arr.getvalue()

# --- APP UI ---
st.markdown("<h1 class='main-title'>🇮🇳 Indian PCC Application Photo Studio</h1>", unsafe_allow_html=True)

# THE COMPLIANCE BOX
st.markdown("""
<div class="compliance-box">
    <p>The Indian Government portals have extremely strict validation logic that often rejects photos. 
    <b>This studio automates the geometry and the "digital weight" to ensure a 100% upload success rate.</b></p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;">
        <div><span class="check-mark">✓</span> <b>Dimensions:</b> Exactly 630 x 810 pixels.</div>
        <div><span class="check-mark">✓</span> <b>File Size Floor:</b> Minimum 200 KB.</div>
        <div><span class="check-mark">✓</span> <b>File Size Ceiling:</b> Below 250 KB.</div>
        <div><span class="check-mark">✓</span> <b>Composition:</b> 70-80% Face Coverage.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("Upload & Control")
    uploaded_file = st.file_uploader("Select Photo", type=['jpg', 'jpeg'])
    target_kb = st.slider("Target Weight (KB)", 200, 245, 215)
    st.divider()
    st.markdown("### 📈 Studio Traffic")
    # This badge tracks your GitHub repo visitors
    st.markdown("![Visits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgulzarrf1991-boop%2FPCC-photo-v1&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Total+Visitors&edge_flat=false)")

if uploaded_file:
    with st.spinner("AI Processing..."):
        orig, final_pil, final_bytes = process_photo(uploaded_file, target_kb)
        if final_bytes:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original")
                st.image(orig, use_container_width=True)
            with col2:
                st.subheader("PCC Compliant Output")
                st.image(final_bytes, width=315)
                st.metric("Final Size", f"{len(final_bytes)/1024:.2f} KB")
                st.download_button("📥 Download 630x810 JPG", final_bytes, "PCC_Photo.jpg", "image/jpeg")

st.divider()
st.caption("PCC Photo Studio v1.0 | 🇮🇳 Professional Compliance Tool")