
import base64
from pathlib import Path

import streamlit as st
from PIL import Image

from recognizer import recognise_handwriting


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Handwriting Assist",
    page_icon="📝",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background-color: #FAF9F6;
        margin: 0;
        padding: 0;
    }

    /* Hide Streamlit header and Deploy bar */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }

    /* Hide menu and footer */
    #MainMenu,
    footer {
        display: none !important;
    }

    /* Remove unwanted top spacing */
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stMain"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
        max-width: none !important;
    }

    .stAppViewContainer .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
        padding-left: 5vw !important;
        padding-right: 5vw !important;
        max-width: none !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #438A85;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #34736F;
        color: white;
    }

    /* Section headings */
    h2, h3 {
        color: #174C5A;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# WEBSITE HEADER / FULL-SCREEN HERO SECTION
# --------------------------------------------------

image_path = Path(__file__).parent / "handwriting_hero_background.png"

if image_path.exists():

    hero_image = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    hero_html = f"""
    <style>

        .hero-section {{

            /* Background photograph */
            background-image:
                linear-gradient(
                    90deg,
                    rgba(250, 247, 242, 0.96) 0%,
                    rgba(250, 247, 242, 0.88) 35%,
                    rgba(250, 247, 242, 0.05) 75%
                ),
                url("data:image/png;base64,{hero_image}");

            /*
            Show the complete photograph without cropping.
            The image may stretch slightly to fit the screen.
            */
            background-size: 100% 100%;
            background-position: center center;
            background-repeat: no-repeat;
            background-color: #FAF7F2;

            /* Full browser width */
            width: 100vw;
            margin-left: calc(50% - 50vw);
            margin-top: 0;

            /* Full browser height */
            height: 100vh;
            min-height: 650px;

            padding: 65px 10%;

            display: flex;
            flex-direction: column;
            justify-content: center;

            box-sizing: border-box;
            border-radius: 0;
        }}

        /* Main title */
        .hero-title {{
            color: #174C5A;
            font-family: Georgia, serif;
            font-size: 58px;
            font-weight: bold;
            margin-bottom: 12px;
        }}

        /* Subtitle */
        .hero-subtitle {{
            color: #405966;
            font-size: 23px;
            margin-bottom: 22px;
        }}

        /* Decorative divider */
        .hero-divider {{
            width: 90px;
            height: 2px;
            background-color: #438A85;
            margin-bottom: 28px;
        }}

        /* Description */
        .hero-description {{
            color: #263238;
            font-size: 18px;
            line-height: 1.65;
            max-width: 570px;
        }}

        /* Mobile layout */
        @media (max-width: 768px) {{

            .hero-section {{
                min-height: 650px;
                height: 100vh;
                padding: 35px 7%;
                background-position: center center;
            }}

            .hero-title {{
                font-size: 38px;
            }}

            .hero-subtitle {{
                font-size: 17px;
            }}

            .hero-description {{
                font-size: 15px;
                max-width: 100%;
            }}

        }}

    </style>

    <div class="hero-section">

        <div class="hero-title">
            Handwriting Assist
        </div>

        <div class="hero-subtitle">
            AI-powered handwriting recognition for palliative care
        </div>

        <div class="hero-divider"></div>

        <div class="hero-description">
            Handwriting Assist uses artificial intelligence to help
            interpret handwritten messages, including handwriting
            that may be difficult to read due to tremors or reduced
            motor control.
        </div>

    </div>
    """

    st.html(hero_html)

else:

    st.warning(
        "Hero background image not found. "
        "Please ensure handwriting_hero_background.png "
        "is in the same folder as app.py."
    )

    st.title("Handwriting Assist")

    st.subheader(
        "AI-powered handwriting recognition for palliative care"
    )

    st.write(
        "Handwriting Assist uses artificial intelligence to help "
        "interpret handwritten messages, including handwriting "
        "that may be difficult to read due to tremors or reduced "
        "motor control."
    )


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

st.markdown("---")

st.header("Upload Handwriting")

uploaded_file = st.file_uploader(
    "Choose a handwriting image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.success("Image uploaded successfully!")

    st.markdown("---")


    # --------------------------------------------------
    # RECOGNITION
    # --------------------------------------------------

    if st.button(
        "Recognise Handwriting",
        use_container_width=True
    ):

        with st.spinner(
            "Analysing handwriting... Please wait."
        ):

            try:

                recognised_text, average_confidence = (
                    recognise_handwriting(image)
                )

                st.session_state["recognised_text"] = recognised_text

                st.session_state["average_confidence"] = (
                    average_confidence
                )

                st.session_state["recognition_image"] = image

            except Exception as e:

                st.error(
                    f"An error occurred during recognition: {e}"
                )


    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    if "recognised_text" in st.session_state:

        st.markdown("---")

        st.header("Recognition Results")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Original Handwriting")

            st.image(
                st.session_state["recognition_image"],
                use_container_width=True
            )

        with col2:

            st.subheader("Recognised Transcription")

            edited_text = st.text_area(
                "You can edit the recognised text below:",
                value=st.session_state["recognised_text"],
                height=250,
                key="editable_transcription"
            )

            st.caption(
                "Review and edit the transcription where necessary."
            )

            st.download_button(
                label="Download Transcription",
                data=edited_text,
                file_name="handwriting_transcription.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.code(
                edited_text,
                language=None
            )


        # --------------------------------------------------
        # CONFIDENCE DISPLAY
        # --------------------------------------------------

        st.markdown("---")

        st.subheader("Estimated Recognition Confidence")

        confidence = st.session_state.get(
            "average_confidence"
        )

        if confidence is not None:

            confidence_percentage = confidence * 100

            st.metric(
                label="Estimated Confidence",
                value=f"{confidence_percentage:.1f}%"
            )

            st.progress(
                max(0.0, min(float(confidence), 1.0))
            )

            if confidence >= 0.70:

                st.success(
                    "The model produced a relatively high confidence "
                    "estimate. Please still review the transcription."
                )

            else:

                st.warning(
                    "The model produced a lower confidence estimate. "
                    "Carefully check the transcription against the "
                    "original handwriting."
                )

            st.caption(
                "This is an approximate model-generated confidence "
                "score, not a measure of guaranteed transcription accuracy."
            )

        else:

            st.info(
                "A confidence estimate is not available for this result."
            )


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.markdown("---")

st.info(
    "**Disclaimer:** Handwriting Assist is an AI-assisted transcription "
    "tool. Its output may contain errors and should be checked against "
    "the original handwriting. It is not intended to replace human "
    "interpretation or professional judgement."
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        color: #718096;
        font-size: 14px;
        padding: 10px;
    ">
        Handwriting Assist | AI-assisted transcription
    </div>
    """,
    unsafe_allow_html=True
)
