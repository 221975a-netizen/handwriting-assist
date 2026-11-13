
import os
import torch
import streamlit as st

from PIL import Image
from functools import lru_cache
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

MODEL_ID = "221975a/assisted-handwriting-recognition"

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

    processor, model = load_model()

    image = image.convert("RGB")

    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values.to(DEVICE)

    with torch.inference_mode():

        outputs = model.generate(
            pixel_values,
            max_new_tokens=128,
            return_dict_in_generate=True,
            output_scores=True
        )

    generated_ids = outputs.sequences

    recognised_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0].strip()

    # Estimate average generated-token confidence
    if outputs.scores:
        token_confidences = []

        for step, scores in enumerate(outputs.scores):

            token_id = generated_ids[0, step + 1]

            probabilities = torch.softmax(scores[0], dim=-1)

            confidence = probabilities[token_id].item()

            token_confidences.append(confidence)

        average_confidence = (
            sum(token_confidences) / len(token_confidences)
            if token_confidences else 0.0
        )

    else:
        average_confidence = 0.0

    return recognised_text, average_confidence
