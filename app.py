import streamlit as st
import numpy as np
from PIL import Image
from mtcnn import MTCNN
import io
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Indian PCC Photo Studio", layout="wide", page_icon="🇮🇳")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF9933; color: white; border: none; }
    .stButton>button:hover { background-color: #128807; color: white; }
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

    if not results:
        return None, None, "Error: No face detected. Ensure lighting is even."

    # 1. Geometric Logic
    box = results[0]['box']
    keypoints = results[0]['keypoints']
    face_center_x = box[0] + (box[2] / 2)
    eye_y = (keypoints['left_eye'][1] + keypoints['right_eye'][1]) / 2

    scale = 690 / (box[3] / 0.7) 
    crop_w_orig = target_w / scale
    crop_h_orig = target_h / scale
    
    left = face_center_x - (crop_w_orig / 2)
    top = eye_y - (310 / scale)

    if (top + crop_h_orig) > img.size[1]: top = img.size[1] - crop_h_orig
    if top < 0: top = 0

    final_img = img.crop((left, top, left + crop_w_orig, top + crop_h_orig))
    final_img = final_img.resize((target_w, target_h), Image.LANCZOS)

    # 2. Precision Size Adjustment
    img_byte_arr = io.BytesIO()
    final_img.save(img_byte_arr, format='JPEG', quality=95)
    
    current_size_bytes = img_byte_arr.tell()
    target_bytes = target_kb * 1024

    if current_size_bytes < target_bytes:
        padding_needed = target_bytes - current_size_bytes
        img_byte_arr.write(b'\0' * int(padding_needed))
    
    return img, final_img, img_byte_arr.getvalue()

# --- UI DESIGN ---
st.title("🇮🇳 Indian PCC Application Photo Tool")
st.markdown("Automated **630x810px** cropping for Indian Passport/PCC portal compliance.")
st.divider()

# Sidebar for inputs
with st.sidebar:
    st.header("📸 Upload & Settings")
    uploaded_file = st.file_uploader("Select your photo", type=['jpg', 'jpeg'])
    target_kb = st.slider("Target File Size (KB)", 200, 245, 215)
    st.info("The tool will force the file size to be strictly between 200KB and 250KB.")

if uploaded_file:
    if st.button("✨ Generate Professional PCC Photo"):
        with st.spinner("AI analyzing facial geometry..."):
            orig_img, processed_img, result_bytes = process_photo(uploaded_file, target_kb)
            
            if result_bytes:
                # Top Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Target Resolution", f"630 x 810")
                m2.metric("Resulting File Size", f"{len(result_bytes)/1024:.2f} KB")
                m3.metric("Status", "Ready to Upload")
                
                st.divider()

                # Comparison Columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Photo")
                    st.image(orig_img, use_container_width=True)
                    st.caption("Raw input image")

                with col2:
                    st.subheader("PCC Ready Output")
                    st.image(result_bytes, width=350)
                    st.caption("AI Centered, Zoomed, and Size-Corrected")
                    
                    st.download_button(
                        label=f"📥 Download {len(result_bytes)/1024:.0f}KB JPG",
                        data=result_bytes,
                        file_name="PCC_Final_630x810.jpg",
                        mime="image/jpeg"
                    )
            else:
                st.error("Could not find a face. Please use a clearer photo.")
else:
    st.info("👈 Please upload a photo in the sidebar to get started.")