import os
import tempfile

import streamlit as st
from PIL import Image

from ai.inference.predict import predict


st.set_page_config(
    page_title="Potato Leaf Inspector",
    page_icon="🥔",
    layout="centered",
)


st.title("🥔 Potato Leaf Inspector")

st.write(
    "Upload a leaf image to detect whether it is a potato leaf "
    "and identify possible disease."
)


uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"],
)


if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded image",
        use_container_width=True,
    )

    if st.button("Analyze Image"):
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            ) as temp_file:
                temp_path = temp_file.name
                image.save(temp_path, format="JPEG")

            with st.spinner("Analyzing image..."):
                result = predict(temp_path)

            if not result["is_potato_leaf"]:
                st.error("This does not appear to be a potato leaf.")

                st.write(
                    f"Potato leaf probability: "
                    f"{result['potato_probability']:.2%}"
                )

                st.write(result["recommendation"])

            else:
                st.success("Potato leaf detected!")

                st.subheader("Prediction")

                st.write(
                    f"**Disease:** {result['prediction']}"
                )

                st.write(
                    f"**Confidence:** "
                    f"{result['confidence']:.2%}"
                )

                st.write(
                    f"**Confidence level:** "
                    f"{result['confidence_level']}"
                )

                st.subheader("Explanation")
                st.write(result["explanation"])

                st.subheader("Recommendation")
                st.write(result["recommendation"])

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)