from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import router

app = FastAPI(title="Research2Video MVP")

origins = [
    "http://localhost:3000",  # React frontend URL during development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory where manim outputs videos
MANIM_OUTPUT_DIR = "media/videos"
os.makedirs(MANIM_OUTPUT_DIR, exist_ok=True)

# Mount static route for videos
app.mount("/animations", StaticFiles(directory=MANIM_OUTPUT_DIR), name="animations")

app.include_router(router)