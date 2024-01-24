import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Add the /app directory to the Python path
sys.path.append("/app")

from stablediffusion.txt2img import generate_image as txt2img_generate_image

app = FastAPI()

# Directory to store generated images
DATA_DIR = "/app/data"
os.makedirs(DATA_DIR, exist_ok=True)

class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate_image")
def generate_image(request: ImageRequest):
    prompt = request.prompt
    checkpoint_path = "/models/stable-diffusion/768model.ckpt"
    config_path = "configs/stable-diffusion/v2-inference-v.yaml"
    output_image_path = os.path.join(DATA_DIR, "generated_image.png")

    try:
        # Import and run the txt2img script directly
        txt2img_generate_image(prompt, checkpoint_path, config_path, output_image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running txt2img.py script: {e}")

    return FileResponse(path=output_image_path, filename="generated_image.png")
