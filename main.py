from fastapi import FastAPI
import os

# Create the FastAPI app instance
app = FastAPI()

# Default route — for testing Render
@app.get("/")
def home():
    return {"message": "✅ Mapoho AI backend is live and running!"}


# Optional: example route for testing environment variables
@app.get("/env-check")
def env_check():
    key = os.getenv("OPENAI_API_KEY")
    return {"has_key": bool(key)}

