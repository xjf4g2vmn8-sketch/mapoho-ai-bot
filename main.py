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

# ===============================
#  MAPOHO AI – Callback Endpoint (Fixed & Tested)
# ===============================
from fastapi import Form
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
import os

@app.post("/api/callback")
async def callback_request(
    name: str = Form(...),
    phone: str = Form(...),
    message: str = Form("")
):
    # Email body content
    body = f"""
    New Callback Request from Mapoho AI Bot

    Name: {name}
    Phone: {phone}
    Message: {message}
    """

    # Create email message object (this is what fixes the "msg not defined" error)
    msg = MIMEText(body)
    msg["Subject"] = "Callback Request from Mapoho AI"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("ADMIN_EMAIL")

    try:
        # Connect to Afrihost SMTP
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)

        return JSONResponse({"status": "success", "message": "Callback request sent successfully"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})
