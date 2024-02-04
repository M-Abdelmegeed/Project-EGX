from flask import Flask, request
import random
from chatbot import chatbot

app = Flask(__name__)

@app.route('/', methods=['POST'])
def dummy_route():
    responses = ["Hello!", "Welcome to the dummy route!", "Flask is fun!", "Random text here!"]
    return random.choice(responses)

@app.route('/chatbot', methods=['POST'])
def chat():
    try:
        request_data = request.get_json()

        session_id = request_data.get("session_id")
        message = request_data.get("message")

        response = chatbot(session_id=session_id, user_input=message, llm='Gemini')
        return {"output": response}
    except Exception as e:
        return [], 500

if __name__ == '__main__':
    app.run(debug=True, port=5555)
