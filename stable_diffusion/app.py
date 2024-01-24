from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from pathlib import Path
import logging
from huggingface_hub import login
import os


logger = logging.getLogger(__name__)
app = FastAPI()

class ImageRequest(BaseModel):
    prompt: str

# get your account token from https://huggingface.co/settings/tokens
token = os.getenv("HF_TOKEN")


@app.post("/generate_image")
def generate_image(request: ImageRequest):
    try:
        pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", use_safetensors=True, token=token)
        if torch.cuda.is_available():
            pipe.to("cuda")
        images = pipe(request.prompt).images

        output = Path("./data")
        output.mkdir(parents=True, exist_ok=True)
        for i in range(len(images)):
            images[i].save(output / f"{i}.png")

        return {"message": "Image generation successful"}
    except Exception as e:
        error_message = f"An error occurred during image generation: {str(e)}"
        logger.exception(error_message)
        return {"error": error_message}, 500