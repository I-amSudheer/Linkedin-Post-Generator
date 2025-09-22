from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests, os

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/generatePost/")
async def generate_post(request: Request):
    res = await request.json()
    topic = res.get("topic")
    
    if not topic:
        return {"error": "Missing 'topic' in request body."}

    # Use your real API key here
    api_key = os.getenv("GROQ_API_KEY") 
    print("DEBUG: API Key used:", api_key[:4] + "...")

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": topic}
        ],
        "model": "llama-3.3-70b-versatile"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }   

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        data = response.json()
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

    if "error" in data:
        return {"error": data["error"].get("message", "Unknown API error")}

    if "choices" in data and len(data["choices"]) > 0:
        post_content = data["choices"][0]["message"]["content"]
        return {"post": post_content}
    else:
        return {"error": "No content returned by API."}
