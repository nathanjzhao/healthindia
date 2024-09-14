from flask import Flask, request, jsonify
from flask_cors import CORS
from healthBot import handle_chat
import os

app = Flask(__name__)

# Configuring CORS to allow requests from your frontend's origin
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    print(f"Received data: {data}")  # Debugging line
    user_message = data.get('message')
    user_info = data.get('userInfo', {})
    history = data.get('history', [])

    try:
        response = handle_chat(user_message, user_info, history)
        return jsonify(response)
    except Exception as e:
        print(f"Error in chat route: {str(e)}")  # Debugging line
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    app.run(debug=True)
print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}")
