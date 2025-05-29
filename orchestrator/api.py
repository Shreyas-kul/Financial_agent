from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import whisper
import numpy as np
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.crew_manager import FinancialCrew
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize Whisper model for STT
try:
    logger.info("Loading Whisper model...")
    model = whisper.load_model("base")
    logger.info("Whisper model loaded successfully")
except Exception as e:
    logger.error(f"Error loading Whisper model: {str(e)}")
    model = None

class AudioInput(BaseModel):
    audio_data: List[float]
    sample_rate: int

class TextInput(BaseModel):
    text: str

@app.post("/process_audio")
async def process_audio(audio_input: AudioInput):
    try:
        logger.info("Processing audio input...")
        if model is None:
            raise HTTPException(status_code=500, detail="Speech recognition model not initialized")
            
        # Convert audio data to format expected by Whisper
        audio_array = np.array(audio_input.audio_data)
        
        # Transcribe audio
        logger.info("Transcribing audio...")
        result = model.transcribe(audio_array)
        transcribed_text = result["text"]
        logger.info(f"Transcribed text: {transcribed_text}")
        
        # Process with crew
        logger.info("Processing with CrewAI...")
        crew = FinancialCrew()
        response = crew.run_crew()
        logger.info("CrewAI processing complete")
        
        return {
            "transcribed_text": transcribed_text,
            "response": response
        }
    except Exception as e:
        logger.error(f"Error in process_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_text")
async def process_text(text_input: TextInput):
    try:
        logger.info(f"Processing text input: {text_input.text}")
        crew = FinancialCrew()
        response = crew.run_crew()
        logger.info("CrewAI processing complete")
        
        return {
            "response": response
        }
    except Exception as e:
        logger.error(f"Error in process_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "whisper_model": "loaded" if model is not None else "not loaded"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 