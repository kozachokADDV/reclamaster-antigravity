import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VIBER_TOKEN = os.getenv("VIBER_AUTH_TOKEN")
INSTAGRAM_VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PORT = int(os.getenv("PORT", 5000))

# --- Utils ---
def process_message(platform, user_id, message_text):
    """
    Central function to process messages from all platforms.
    """
    logger.info(f"Received message from {platform} (User: {user_id}): {message_text}")
    
    response_text = f"Привіт! Я отримав твоє повідомлення з {platform}: {message_text}"
    
    if platform == 'telegram':
        send_telegram_message(user_id, response_text)
    elif platform == 'viber':
        send_viber_message(user_id, response_text)
    elif platform == 'instagram':
        send_instagram_message(user_id, response_text)

# --- Telegram Logic ---
import requests

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    update = request.json
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text:
            process_message("telegram", chat_id, text)
    return "OK", 200

# --- Viber Logic ---
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest

viber = Api(BotConfiguration(
    name='MyMultichannelBot',
    avatar='http://site.com/avatar.jpg',
    auth_token=VIBER_TOKEN
))

def send_viber_message(user_id, text):
    viber.send_messages(user_id, [TextMessage(text=text)])

@app.route('/viber', methods=['POST'])
def viber_webhook():
    # Verify request signature
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return "Invalid signature", 403
    
    viber_request = viber.parse_request(request.get_data())
    
    if isinstance(viber_request, ViberMessageRequest):
        process_message("viber", viber_request.sender.id, viber_request.message.text)
        
    return "OK", 200

# --- Instagram Logic ---
def send_instagram_message(user_id, text):
    # This requires a valid Graph API Access Token
    pass 

@app.route('/instagram', methods=['GET', 'POST'])
def instagram_webhook():
    if request.method == 'GET':
        # Verification request from Facebook
        verify_token = request.args.get("hub.verify_token")
        if verify_token == INSTAGRAM_VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Invalid verification token", 403
    
    elif request.method == 'POST':
        data = request.json
        if data.get("object") == "instagram":
             for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    if "message" in messaging_event:
                        sender_id = messaging_event["sender"]["id"]
                        text = messaging_event["message"].get("text", "")
                        process_message("instagram", sender_id, text)
        return "EVENT_RECEIVED", 200

@app.route('/')
def home():
    return "Bot Server is Running!"

if __name__ == '__main__':
    app.run(port=PORT)
