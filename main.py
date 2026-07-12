from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

# Allow your iOS frontend to securely communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Payload(BaseModel):
    description: str

STOP_WORDS = {"the", "a", "and", "is", "in", "it", "you", "of", "to", "for", "with", "on", "this", "my", "that"}

@app.post("/generate")
def generate_hashtags(payload: Payload):
    text = payload.description.lower()
    # Remove punctuation and pull individual words
    words = re.findall(r'\b\w+\b', text)
    
    # Filter keywords based on length and common stop words
    keywords = [f"#{w}" for w in words if w not in STOP_WORDS and len(w) > 2]
    keywords = list(dict.fromkeys(keywords))[:7] # Deduplicate and cap at 7 custom contextual tags
    
    # Mix dynamic tags with viral TikTok anchor constants
    viral_anchors = ["#fyp", "#foryoupage", "#trending", "#viral", "#xyzbca"]
    
    final_tags = keywords + [tag for tag in viral_anchors if tag not in keywords]
    
    return {"hashtags": final_tags[:12]} # Limit total tags to maximize readability
