import json
import os
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Verification token for WhatsApp webhook
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Set in .env file

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Handle webhook verification
        hub_mode = request.args.get("hub.mode")
        hub_challenge = request.args.get("hub.challenge")
        hub_verify_token = request.args.get("hub.verify_token")
        
        if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN and hub_challenge:
            print("Webhook verified successfully")
            return hub_challenge, 200
        else:
            return "<p>Verification failed</p>", 403

    if request.method == "POST":
        try:
            # Log incoming webhook data
            data = request.get_json()
            print(json.dumps(data, indent=4))
            
            # Basic acknowledgment of message receipt
            if (
                data.get("object") == "whatsapp_business_account"
                and data.get("entry")
                and len(data["entry"]) > 0
                and data["entry"][0].get("changes")
                and len(data["entry"][0]["changes"]) > 0
            ):
                return "<p>Webhook POST received</p>", 200
            else:
                return "<p>Invalid payload</p>", 400
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return "<p>Error processing webhook</p>", 500

if __name__ == "__main__":
    app.run(debug=True)