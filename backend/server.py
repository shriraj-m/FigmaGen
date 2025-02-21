from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

# Set up logging
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

# Define request structure
class PromptRequest(BaseModel):
    prompt: str

# Define a response structure (modify as needed)
class DesignResponse(BaseModel):
    elements: list  # List of UI elements (e.g., buttons, frames)

@app.post("/generate-ui/")
async def generate_ui(request: PromptRequest, raw_request: Request):
    logger.info(f"Received request with prompt: {request.prompt}")
    # logger.info(f"Request headers: {raw_request.headers}")
    
    prompt = request.prompt
    # TODO: Integrate your AI agentic setup here
    generated_ui = [
        {"type": "frame", "width": 400, "height": 300, "name": "Generated Frame"},
        {"type": "text", "content": "Hello, AI!"}
    ]
    
    response = {"elements": generated_ui}
    # logger.info(f"Sending response: {response}")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
