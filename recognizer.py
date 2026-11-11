
import os
import torch
import streamlit as st

from PIL import Image
from functools import lru_cache
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Hugging Face repository containing your trained model
MODEL_ID = "221975a/assisted-handwriting-recognition"

# Use CPU initially for reliable compatibility
DEVICE = torch.device("cpu")


def get_hf_token():
    """Retrieve the Hugging Face token securely."""

    token = os.environ.get("HF_TOKEN")

    if not token:
        try:
            token = st.secrets["HF_TOKEN"]
        except (KeyError, FileNotFoundError):
            token = None

    if not token:
        raise RuntimeError(
            "Hugging Face token not found. "
            "Please configure HF_TOKEN in Streamlit Secrets."
        )

    return token


@lru_cache(maxsize=1)
def load_model():

    print("Loading trained TrOCR model from Hugging Face...")

    token = get_hf_token()

    processor = TrOCRProcessor.from_pretrained(
        MODEL_ID,
        token=token
    )

    model = VisionEncoderDecoderModel.from_pretrained(
        MODEL_ID,
        token=token
    )

    model.to(DEVICE)
    model.eval()

    print("TrOCR model loaded successfully!")

    return processor, model


def recognise_handwriting(image):

    # Load model and processor
    processor, model = load_model()

    # Ensure image is RGB
    image = image.convert("RGB")

    # Process handwriting image
    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values.to(DEVICE)

    # Generate handwritten text prediction
    with torch.inference_mode():

        generated_ids = model.generate(
            pixel_values,
            max_new_tokens=128
        )

    # Convert model output into readable text
    recognised_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return recognised_text.strip()


