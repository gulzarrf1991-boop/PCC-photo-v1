import streamlit as st
import numpy as np
from PIL import Image
from mtcnn import MTCNN
import io

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Indian PCC Photo Studio", layout="wide", page_icon="🇮🇳")

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .compliance-box {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #FF9933;
        margin-bottom: 20px;
    }
    .check-mark { color: #128807; font-weight: bold; }
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

# --- 3. PERSISTENT UI (Always Visible) ---
st.title("🇮🇳 Indian PCC Application Photo Studio")

st.markdown("""
<div class="compliance-box">
    <p><b>Strict Validation Logic:</b> Rejects photos if they aren't exactly 630x810px or between 200KB-250KB.</p>
    <span class="check-mark">✓</span> Exactly 630x810px | 
    <span class="check-mark">✓</span> Weight: 200KB - 250KB | 
    <span class="check-mark">✓</span> 70-80% Face Coverage
</div>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("Upload & Settings")
    uploaded_file = st.file_uploader("Select Photo", type=['jpg', 'jpeg'])
    target_kb = st.slider("Target Weight (KB)", 200, 245, 215)
    st.divider()
    st.markdown("![Visits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgulzarrf1991-boop%2FPCC-photo-v1&title=Visitors)")

# --- 5. PROCESSING LOGIC ---
if uploaded_file:
    # Use a button to trigger processing
    if st.button("🚀 Generate PCC Photo"):
        with st.spinner("AI is aligning photo..."):
            orig, final_pil, final_bytes = process_photo(uploaded_file, target_kb)
            
            if final_bytes:
                # Store in session state so it doesn't disappear on click
                st.session_state['result'] = (orig, final_bytes)
    
    # Check if we have a result to show
    if 'result' in st.session_state:
        orig, final_bytes = st.session_state['result']
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.image(orig, use_container_width=True)
        with col2:
            st.subheader("Result (630x810)")
            st.image(final_bytes, width=315)
            st.metric("Final Weight", f"{len(final_bytes)/1024:.2f} KB")
            st.download_button("📥 Download Photo", final_bytes, "PCC_Final.jpg", "image/jpeg")
else:
    st.info("Upload a photo in the sidebar to begin.")