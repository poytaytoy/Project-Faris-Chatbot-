import os
import time
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from chat import runConversation
from voice import generateVoice, processCode
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ResourceRequest(BaseModel):
    location: str

class AudioRequest(BaseModel):
    token: str

class ChatRequest(BaseModel):
    message: str
    sentMemory: List


def delete_audio_task(token: str):
    """Background task to delete audio after serving."""
    time.sleep(1)
    file_path = os.path.join(os.getcwd(), 'audioResult', f"{token}.wav")
    if os.path.exists(file_path):
        os.remove(file_path)


@app.post("/Resources")
async def resources(req: ResourceRequest):
    file_location = req.location[4:]
    
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Resource not found")

    extension = os.path.splitext(file_location)[1].lower()
    
    # Logic fix: Original code had a bug returning 'mimetypes2' (None)
    mimetype = "application/octet-stream"
    if extension == '.png':
        mimetype = "image/png"
    elif extension == '.json':
        mimetype = "application/json"

    return FileResponse(file_location, media_type=mimetype)

@app.get("/Resources/vtuber hood on/vtuber hood on.1024/texture_00.png")
async def resources_png():
    path = "Resources/vtuber hood on/vtuber hood on.2048/texture_00.png"
    return FileResponse(path, media_type="image/png")

@app.post("/audioBeg")
async def get_audio(req: AudioRequest, background_tasks: BackgroundTasks):
    location = req.token
    file_path = f'audioResult/{location}.wav'
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    background_tasks.add_task(delete_audio_task, location)
    
    return FileResponse(file_path, media_type='audio/wav')

@app.post("/returnResponse")
async def return_response(req: ChatRequest):
    try: 
        response_text, memory = runConversation(req.message, req.sentMemory)
        if response_text != '':
            processed_response = processCode(response_text)
            token, length = generateVoice(processed_response)
            
            return {
                'response': [{
                    'message': response_text, 
                    'token': token, 
                    'mood': "exp_05", 
                    'time': length
                }], 
                'sentMemory': memory
            }
        return {"response": [], "sentMemory": req.sentMemory}

    except Exception: 
        token, length = generateVoice('what?')
        return {
            'response': [
                {'message': 'what?', 'token': token, 'mood': 'exp_05', 'time': length},
                req.sentMemory
            ], 
            'sentMemory': req.sentMemory
        }