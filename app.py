import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="MagicCrop", page_icon="✨")

st.title("✨ MagicCrop - AI Background Remover")
st.write("আপনার ছবির ব্যাকগ্রাউন্ড মুহূর্তেই রিমুভ করুন একদম ফ্রিতে!")

uploaded_file = st.file_uploader("একটি ছবি আপলোড করুন", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file).convert("RGBA")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(input_image, use_container_width=True)
        
    with st.spinner("ব্যাকগ্রাউন্ড রিমুভ করা হচ্ছে..."):
        output_image = remove(input_image)
        
    with col2:
        st.subheader("Background Removed")
        st.image(output_image, use_container_width=True)
        
    # Download Button
    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    
    st.download_button(
        label="Download Image 📥",
        data=buf.getvalue(),
        file_name="magiccrop_output.png",
        mime="image/png"
    )
  
