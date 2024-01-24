import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

app = FastAPI()

# Directory to store generated images
DATA_DIR = "/app/data"
os.makedirs(DATA_DIR, exist_ok=True)

class ImageRequest(BaseModel):
    prompt: str

model_id = "file:///models/stable-diffusion"

@app.post("/generate_image")
def generate_image(request: ImageRequest):
    prompt = request.prompt
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(prompt).images[0]
    output_image_path = os.path.join(DATA_DIR, "generated_image.png")
    image.save(output_image_path)
    return FileResponse(path=output_image_path, filename="generated_image.png")