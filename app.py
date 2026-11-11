
import streamlit as st
from PIL import Image
from recognizer import recognise_handwriting
# Configure website
st.set_page_config(
    page_title="Handwriting Assist",
    page_icon="✍️",
    layout="wide"
)

# Website heading
st.title("✍️ Handwriting Assist")

st.subheader(
    "AI-powered handwriting recognition for palliative care"
)

st.write(
    "Upload an image of handwritten text. "
    "Our AI system will help interpret difficult "
    "or tremulous handwriting."
)

st.divider()

# Image upload
st.header("Upload Handwriting")

uploaded_file = st.file_uploader(
    "Choose a handwriting image",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Your Uploaded Handwriting")

    st.image(
        image,
        caption="Original handwriting",
        use_container_width=True
    )

    st.success("Image uploaded successfully!")

    if st.button("Recognise Handwriting"):

        with st.spinner("AI is analysing your handwriting..."):

            try:
                recognised_text = recognise_handwriting(image)

                st.subheader("Recognised Handwriting")

                if recognised_text:
                    st.success("Recognition completed!")

                    st.text_area(
                        "AI Transcription",
                        value=recognised_text,
                        height=150
                    )

                else:
                    st.warning(
                        "The AI could not recognise any text."
                    )

            except Exception as e:
                st.error(f"Recognition failed: {e}")

else:
    st.info("Please upload an image to begin.")

st.divider()

st.caption(
    "Handwriting Assist | AI-assisted transcription"
)
