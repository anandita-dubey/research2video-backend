from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.pdf_extractor import extract_text_from_pdf
from app.summarizer import generate_summary_script
from app.visual_generator import generate_animation
from openai import OpenAI
import os
import json
import re
import math

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculate_max_tokens(text: str, base: int = 500, max_cap: int = 2000) -> int:
    estimated_tokens = math.ceil(len(text.split()) * 1.3)
    return min(max(base, estimated_tokens), max_cap)

@router.post("/upload-paper/")
async def upload_paper(file: UploadFile = File(...), length: str = Form("medium")):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF or file is empty.")

    script = generate_summary_script(text, length)
    return {"summary_script": script}

class StoryboardRequest(BaseModel):
    summary_text: str

@router.post("/generate-storyboard/")
async def generate_storyboard(request: StoryboardRequest):
    summary = request.summary_text.strip()
    if not summary:
        raise HTTPException(status_code=400, detail="Summary text cannot be empty.")

    max_tokens = calculate_max_tokens(summary)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional video storyboard generator. "
                        "Break the provided summary into 3-5 concise scenes. "
                        "For each scene provide: scene number, a short descriptive text, "
                        "and a visual/animation suggestion. "
                        "Output only valid JSON — an array of objects with 'scene', 'text', and 'visual_hint'."
                    )
                },
                {"role": "user", "content": summary}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        result_text = response.choices[0].message.content.strip()
        print("Raw storyboard response:", result_text)

        cleaned_text = re.sub(r"```json|```", "", result_text).strip()
        storyboard = json.loads(cleaned_text)
        return {"storyboard": storyboard}

    except json.JSONDecodeError:
        print("JSON parsing error. Raw response:", result_text)
        raise HTTPException(status_code=500, detail="Invalid JSON received from model.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")

class VisualRequest(BaseModel):
    scene_text: str
    style: str = "style1"

@router.post("/generate-visuals/")
async def generate_visuals(request: VisualRequest):
    scene_text = request.scene_text.strip()
    style = request.style

    if not scene_text:
        raise HTTPException(status_code=400, detail="Scene text cannot be empty.")

    try:
        video_filename = generate_animation(scene_text, style)
        video_path = f"/animations/{video_filename}"  # Match static mount URL
        return {"video_path": video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visual generation error: {e}")