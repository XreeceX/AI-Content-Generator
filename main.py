import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Content Generator API")

# CORS: configurable via CORS_ORIGINS env (comma-separated) or defaults
_cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContentRequest(BaseModel):
    input_text: str


# Load model lazily to avoid startup delay
_text_generator = None


def get_generator():
    global _text_generator
    if _text_generator is None:
        _text_generator = pipeline("text-generation", model="gpt2")
    return _text_generator


@app.post("/generate")
async def generate_content(request: ContentRequest):
    text = (request.input_text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="input_text cannot be empty")
    try:
        generator = get_generator()
        generated = generator(
            text,
            max_length=100,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.8,
        )
        generated_text = generated[0]["generated_text"]
        return {"generated_content": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
