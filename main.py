from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ Mapoho AI backend is live and running!"}


@app.api_route("/chat", methods=["GET", "POST"])
async def chat(request: Request):
    if request.method == "GET":
        return {
            "info": "Send a POST request with JSON { 'message': 'your text' } "
                    "to receive a Mapoho AI response."
        }

    try:
        data = await request.json()
        user_message = data.get("message", "")
        if not user_message:
            return {"error": "No message provided"}

        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Use new chat completion API syntax
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Mapoho AI, a friendly insurance assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=250,
        )

        reply = completion.choices[0].message.content.strip()
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
msg["Subject"] = "Callback Request from Mapoho AI"
From: info@mapoho.co.za
To: info@mapoho.co.za

