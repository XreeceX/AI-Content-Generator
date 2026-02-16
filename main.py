from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS so frontend (on a different port) can communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the model for incoming requests
class ContentRequest(BaseModel):
    input_text: str

# Load GPT-2 model for text generation
text_generator = pipeline("text-generation", model="gpt2")

# Define a POST endpoint for generating content
@app.post("/generate")
async def generate_content(request: ContentRequest):
    # Use the text_generator pipeline to generate content
    generated = text_generator(request.input_text, max_length=100, num_return_sequences=1)
    
    # Extract the generated text
    generated_text = generated[0]["generated_text"]
    
    return {"generated_content": generated_text}
