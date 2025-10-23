from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Initialize FastAPI app
app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your website domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def home():
    return {"message": "✅ Mapoho AI backend is live and running!"}


# 🧩 CHAT ENDPOINT
@app.post("/chat")
async def chat(request: Request):
    """
    Receives a message from frontend, sends it to OpenAI, returns AI response.
    """
    try:
        data = await request.json()
        user_message = data.get("message", "")

        if not user_message:
            return {"error": "No message provided"}

        # Get your OpenAI API key from environment variables
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Make API request to OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Mapoho AI, a friendly insurance assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=250,
        )

        reply = completion.choices[0].message["content"].strip()
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
