from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
import json

from main import call_agent_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware for Figma connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-ui/")
async def generate_ui(request: PromptRequest, raw_request: Request):
    logger.info(f"Received request with prompt: {request.prompt}")
    # logger.info(f"Request headers: {raw_request.headers}")

    prompt = request.prompt    
    # get  raw response from  agent
    raw_response = call_agent_workflow(prompt)
    
    try:
        # remove any surrounding quotes, replace escaped newlines with actual newlines
        cleaned_response = raw_response.strip("'")
        cleaned_response = cleaned_response.replace('\\n', '\n')
        # parse as JSON to ensure valid format
        generated_ui = json.loads(cleaned_response)
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        return {"error": "Invalid JSON response from agent"}
    
    print(generated_ui)
    response = {"elements": [generated_ui]}
    
    # logger.info(f"Sending response: {response}")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
