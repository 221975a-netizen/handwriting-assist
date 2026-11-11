
import torch
from pathlib import Path
from PIL import Image
from functools import lru_cache
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Locate your trained model
MODEL_PATH = Path(__file__).parent / "pilot_500_steps"

# Use CPU initially for reliable compatibility
DEVICE = torch.device("cpu")


@lru_cache(maxsize=1)
def load_model():

    print("Loading trained TrOCR model...")

    processor = TrOCRProcessor.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    model = VisionEncoderDecoderModel.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
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

