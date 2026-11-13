
import streamlit as st
from PIL import Image
from recognizer import recognise_handwriting

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Handwriting Assist",
    page_icon="✍️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F5F8FA;
}

/* Main content width */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Main heading */
.main-title {
    color: #174C5A;
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    color: #647985;
    font-size: 17px;
    margin-bottom: 25px;
}

/* Section headings */
h2, h3 {
    color: #174C5A !important;
}

/* Buttons */
.stButton > button {
    background-color: #247C83;
    color: white;
    border-radius: 9px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background-color: #195E65;
    color: white;
}

/* Download button */
.stDownloadButton > button {
    background-color: #E5F1F1;
    color: #174C5A;
    border: 1px solid #B7D5D5;
    border-radius: 9px;
    font-weight: 600;
    width: 100%;
}

/* Information text */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Footer */
.footer {
    color: #81939B;
    text-align: center;
    font-size: 13px;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "recognised_text" not in st.session_state:
    st.session_state.recognised_text = ""

if "edited_transcription" not in st.session_state:
    st.session_state.edited_transcription = ""

if "confidence" not in st.session_state:
    st.session_state.confidence = None


# --------------------------------------------------
# WEBSITE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">✍️ Handwriting Assist</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered handwriting recognition for palliative care'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
Handwriting Assist uses artificial intelligence to help interpret
handwritten messages, including handwriting that may be difficult
to read due to tremors or reduced motor control.
""")

st.divider()


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

st.header("Upload Handwriting")

st.write(
    "Upload a clear image of handwritten text to begin."
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["png", "jpg", "jpeg"],
    help="Supported formats: PNG, JPG and JPEG."
)


if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.success("Image uploaded successfully!")

    # --------------------------------------------------
    # RECOGNITION BUTTON
    # --------------------------------------------------

    if st.button("✦ Recognise Handwriting"):

        with st.spinner(
            "Analysing handwriting... Please wait."
        ):

            try:
                recognised_text, confidence = recognise_handwriting(image)

                st.session_state.recognised_text = recognised_text
                st.session_state.edited_transcription = recognised_text
                st.session_state.confidence = confidence

            except Exception as e:
                st.error(f"Recognition failed: {e}")

    st.divider()

    # --------------------------------------------------
    # SIDE-BY-SIDE DISPLAY
    # --------------------------------------------------

    left_column, right_column = st.columns(
        2,
        gap="large"
    )

    with left_column:

        st.subheader("Original Handwriting")

        st.image(
            image,
            use_container_width=True
        )

        st.caption(
            "Original image uploaded by the user."
        )

    with right_column:

        st.subheader("AI Transcription")

        if st.session_state.recognised_text:

            st.success("Recognition completed!")

            # Estimated confidence
            confidence = st.session_state.confidence

            if confidence is not None:

                st.write(
                    f"Estimated recognition confidence: {confidence:.1%}"
                )

                if confidence < 0.70:

                    st.warning(
                        "The AI may be uncertain about this transcription. "
                        "Please check the original handwriting carefully."
                    )

                else:

                    st.info(
                        "Please review the transcription against the original "
                        "handwriting, even if the estimated confidence is high."
                    )

            else:

                st.warning(
                    "An estimated confidence score is unavailable. "
                    "Please review the transcription carefully."
                )

            # Editable transcription
            st.text_area(
                "Review and edit the recognised text:",
                key="edited_transcription",
                height=200
            )

            edited_text = st.session_state.edited_transcription

            st.caption(
                "You can correct any words that the AI has "
                "misinterpreted."
            )

            # Copyable text block
            st.write("**Copy transcription**")

            st.code(
                edited_text,
                language=None
            )

            # Download transcription
            st.download_button(
                label="⬇ Download Transcription",
                data=edited_text,
                file_name="handwriting_transcription.txt",
                mime="text/plain",
                use_container_width=True
            )

        else:

            st.info(
                "Your recognised handwriting will appear here "
                "after you click the recognition button."
            )

else:

    st.info(
        "Please upload a handwriting image to begin."
    )


# --------------------------------------------------
# IMPORTANT DISCLAIMER
# --------------------------------------------------

st.divider()

st.subheader("Important Information")

st.warning(
    "This application provides AI-assisted transcription only. "
    "AI recognition may contain errors, especially when handwriting "
    "is severely degraded. All transcriptions must be checked by "
    "a human before being treated as a patient's actual wishes, "
    "instructions or medical information."
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    Handwriting Assist | AI-assisted transcription for palliative care
</div>
""", unsafe_allow_html=True)
