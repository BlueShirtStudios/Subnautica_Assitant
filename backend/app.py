from flask import Flask, jsonify, render_template, request
import main_config
from ai_assitant import AI_Agent
import json
import os

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

ALT = AI_Agent(api=main_config.CONFIGS["api"],
                prompt=main_config.CONFIGS["system_prompt"])

print("CWD:", os.getcwd())
ALT.intitalize_agent()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    if not request.json or 'question' not in request.json:
        return jsonify({"error": "Bad request, 'question' field is missing"}), 400

    user_question = request.json['question']

    try:
        response_text = ALT._handle_message(ALT.chat_session, user_question)
    
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)