# Research2Video MVP

This is the MVP backend for a platform that converts research papers into 3Blue1Brown-style narrated videos.

## Setup Instructions

1. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key in the environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

4. Run the FastAPI app:
```bash
uvicorn main:app --reload
```

5. Test the upload endpoint by sending a PDF file to:
```
POST http://localhost:8000/upload-paper/
```

You will receive a JSON response with a summary script generated from the paper.

---

Feel free to extend the project by adding animation generation, narration, and video assembly modules.
