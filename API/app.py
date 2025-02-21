
import streamlit as st
import requests
from PIL import Image
import io

# FastAPI backend URL
API_URL = "http://localhost:8000/predict"

# Streamlit UI
st.set_page_config(page_title="Potato Disease Classification", layout="centered")
st.title("🥔 Potato Disease Classification")

st.write("Upload an image of a potato leaf to detect disease.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format=image.format)
    img_bytes = img_bytes.getvalue()

    # Predict button
    if st.button("Predict"):
        with st.spinner("Analyzing..."):
            # Send image to FastAPI
            files = {"file": ("image.jpg", img_bytes, "image/jpeg")}
            response = requests.post(API_URL, files=files)

            if response.status_code == 200:
                result = response.json()
                st.success(f"Prediction: **{result['class']}**")
                st.info(f"Confidence: **{result['confidence']*100:.2f}%**")
            else:
                st.error("Error in prediction. Please try again.")

st.markdown("---")
st.write("Developed by **Bhupendra Mewada**")
