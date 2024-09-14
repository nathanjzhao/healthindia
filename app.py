from flask import Flask, request, jsonify
from healthBot import handle_chat  # Import the function from healthBot.py
from flask_cors import CORS  # For handling cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Define the route for the chat API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json  # Get the JSON data from the request
    user_message = data.get('message')
    user_info = data.get('userInfo')

    # Call the function from healthBot.py to process the user's message
    response_text = handle_chat(user_message, user_info)
    
    # Return the response as JSON
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
