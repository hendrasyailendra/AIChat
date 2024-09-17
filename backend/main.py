# uvicorn main:app --reload
import os

import openai
from decouple import config
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from mangum import Mangum

# Get Environment Vars
openai.organization = config("OPEN_AI_ORG", default=os.environ.get("OPEN_AI_ORG"))
openai.api_key = config("OPEN_AI_KEY", default=os.environ.get("OPEN_AI_KEY"))

# Custom function imports
from functions.database import reset_message, store_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

app = FastAPI()
handler = Mangum(app)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def check_health():
    return {"message": "OK"}

@app.get("/reset")
async def reset_messages():
    reset_message()
    return {"message": "Conversation reset"}

@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    #audio_input = open("real.mp3", "rb")

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    audio_input = open(file.filename, "rb")

    message_decoded = convert_audio_to_text(audio_input)
    if not message_decoded:
        return HTTPException(status_code=500, detail="failed to convert")
    
    chat_response = get_chat_response(message_decoded)
    if not chat_response:
        return HTTPException(status_code=500, detail="GPT failed to response")
    store_messages(message_decoded, chat_response)

    audio_output = convert_text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=500, detail="failed to get audio response")
    
    def iterfile():
        yield audio_output
    
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

