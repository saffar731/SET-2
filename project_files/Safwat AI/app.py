import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# REPLACE THIS with your actual API Key
API_KEY = "AIzaSyCnsWXrKKiL3M9BdS7r3a7yaz0Iq1Pa00w"
# Note: Using gemini-1.5-flash as gemini-2.5 is not a standard public endpoint yet
MODEL_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# The requested System Prompt
SYSTEM_INSTRUCTION = {
    "parts": [{"text": "You are Safwat AI created by Safwat rakhwan . you can generate diiferent types of code and answer. if somw one ask about you or me tell ' I am Safwat AI created by Safwat Rakhwan'"}]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    payload = {
        "system_instruction": SYSTEM_INSTRUCTION,
        "contents": [{"parts": [{"text": user_message}]}]
    }
    
    try:
        response = requests.post(MODEL_ENDPOINT, json=payload)
        response.raise_for_status()
        data = response.json()
        bot_reply = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    img_b64 = data.get('image_data')
    mime_type = data.get('mime_type')
    user_text = data.get('message', "Please provide a professional and concise analysis of this image.")
    
    payload = {
        "system_instruction": SYSTEM_INSTRUCTION,
        "contents": [{
            "parts": [
                {"text": user_text},
                {"inline_data": {"mime_type": mime_type, "data": img_b64}}
            ]
        }]
    }
    
    try:
        response = requests.post(MODEL_ENDPOINT, json=payload)
        response.raise_for_status()
        data = response.json()
        bot_reply = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "I encountered an error trying to see that image."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=2016)