<<<<<<< HEAD
import logging
from flask import Flask, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from dotenv import load_dotenv
import os
import requests
import time
from flask_cors import CORS  
from tts import text_to_speech

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

# Load environment variables
load_dotenv()

# Twilio and OpenAI credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
ngrok_url = os.getenv('NGROK_URL')

print(f'ngrok_url: {ngrok_url}')

# Twilio client
client = Client(account_sid, auth_token)

def generate_openai_response(transcript):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": transcript}]
    }
    response = requests.post(url, headers=headers, json=data)
    logger.info(f"OpenAI response: {response.status_code}")
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return None

@app.route("/", methods=['GET', 'POST'])
def voice():
    if request.method == 'POST':
        to_number = request.form['to_number']
        to_number = ''.join(filter(str.isdigit, to_number))
        
        if len(to_number) == 10:
            to_number = f"+1{to_number}"
        
        if not to_number.startswith('+') or not to_number[1:].isdigit():
            return "Invalid phone number format. Please use E.164 format.", 400
        
        try:
            twiml = VoiceResponse()
            speech_text = "Hello, this is an AI-assisted call. How can I help you today?"

            # Generate speech file and get S3 URL
            s3_url = text_to_speech(speech_text)
            if s3_url:
                print(f"Audio data URL: {s3_url[:100]}...") # Print first 100 characters of the URL
                twiml.play(s3_url)
            else:
                twiml.say("I'm sorry, I couldn't generate the audio. Let's try again.")

            gather = Gather(input='speech', action=f'{ngrok_url}/handle_input', method='POST', timeout=3)  # Updated action URL
            twiml.append(gather)

            call = client.calls.create(
                twiml=str(twiml),
                to=to_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER')
            )
            logger.info(f"Initiating call to {to_number}. Call SID: {call.sid}")
            return f"Calling {to_number}... Call SID: {call.sid}"
        except Exception as e:
            logger.error(f"Failed to create call: {str(e)}")
            return f"Failed to create call: {str(e)}", 500
    
    return '''
        <form method="post">
            Phone Number: <input type="text" name="to_number" id="to_number">
            <input type="submit" value="Call">
        </form>
    '''

@app.route("/handle_input", methods=['POST'])
def handle_input():
    try:
        logger.info("handle_input called")
        
        user_input = request.form.get('SpeechResult')
        call_sid = request.form.get('CallSid')

        twiml = VoiceResponse()

        if not user_input:
            logger.warning("No speech input received")
            twiml.say("I'm sorry, I didn't catch that. Could you please repeat?")
        else:
            logger.info(f"User input: {user_input}")
            try:
                speech_text = generate_openai_response(user_input)
                logger.info(f"OpenAI response: {speech_text}")

                if speech_text:
                    if speech_text.lower() == "stop call":
                        twiml.say("Thank you for your time. Goodbye!")
                        twiml.hangup()
                    else:
                        # Generate speech file and get S3 URL
                        s3_url = text_to_speech(speech_text)
                        if s3_url:
                            twiml.play(s3_url)
                        else:
                            twiml.say("I'm sorry, I couldn't generate the audio. Let's try again.")
                else:
                    twiml.say("I'm sorry, I couldn't generate a response. Let's try again.")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error calling OpenAI API: {str(e)}")
                twiml.say("I'm sorry, I'm having trouble thinking right now. Let's try again.")

        # Always add a new Gather unless we're hanging up
        if 'hangup' not in twiml.verbs:
            gather = Gather(input='speech', action=f'{ngrok_url}/handle_input', method='POST', timeout=3)
            twiml.append(gather)

        logger.info(f"Returning TwiML: {twiml}")
        
        # Update the call with the new TwiML
        if call_sid:
            try:
                client.calls(call_sid).update(twiml=str(twiml))
                logger.info(f"Updated call {call_sid} with new TwiML")
            except Exception as e:
                logger.error(f"Error updating call {call_sid}: {str(e)}")
        else:
            logger.warning("No CallSid provided, skipping call update")

        return str(twiml)

    except Exception as e:
        logger.error(f"Error in handle_input: {str(e)}", exc_info=True)
        twiml = VoiceResponse()
        twiml.say("I'm sorry, an error occurred. Please try again later.")
        return str(twiml), 500

@app.route("/log_request", methods=['GET', 'POST'])
def log_request():
    logger.info(f"Received request: {request.method}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Form data: {request.form}")
    logger.info(f"JSON data: {request.json}")
    return "Request logged", 200
=======
# from flask import Flask, request
# from twilio.twiml.voice_response import VoiceResponse
# import sqlite3
# import re
# from twilio.rest import Client
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load environment variables from .env file

# app = Flask(__name__)

# # Database setup
# conn = sqlite3.connect('calls.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE IF NOT EXISTS calls
#              (call_sid TEXT, transcript TEXT, name TEXT, phone TEXT)''')
# conn.commit()

# @app.route("/", methods=['GET', 'POST'])
# def voice():
#     if request.method == 'POST':
#         to_number = request.form['to_number']
        
#         # Clean the phone number input
#         to_number = re.sub(r'[^\d]', '', to_number)  # Remove non-digit characters
        
#         # Convert to E.164 format if necessary
#         if len(to_number) == 10 and to_number.isdigit():
#             to_number = f"+1{to_number}"  # Assuming US country code
        
#         # Validate phone number format
#         if not re.match(r'^\+\d{1,15}$', to_number):
#             return "Invalid phone number format. Please use E.164 format.", 400
        
#         # Twilio credentials
#         account_sid = os.getenv('TWILIO_ACCOUNT_SID')
#         auth_token = os.getenv('TWILIO_AUTH_TOKEN')
#         client = Client(account_sid, auth_token)

#         print(account_sid, to_number, auth_token, os.getenv('TWILIO_PHONE_NUMBER'))
        
#         try:
#             call = client.calls.create(
#                 to=to_number,
#                 from_=os.getenv('TWILIO_PHONE_NUMBER'),
#                 url='https://a903-192-12-14-0.ngrok-free.app/'  # URL to handle the call
#             )
#             return f"Calling {to_number}..."
#         except Exception as e:
#             return f"Failed to create call: {str(e)}", 500
    
#     return '''
#         <form method="post" onsubmit="return validatePhoneNumber()">
#             Phone Number: <input type="text" name="to_number" id="to_number">
#             <input type="submit" value="Call">
#         </form>
#         <script>
#             function validatePhoneNumber() {
#                 var phoneNumber = document.getElementById('to_number').value;
#                 var regex = /^\+?\d{10,15}$/;  // E.164 format
#                 if (!regex.test(phoneNumber)) {
#                     alert("Invalid phone number format. Please use E.164 format.");
#                     return false;  // Prevent form submission
#                 }
#                 return true;  // Allow form submission
#             }
#         </script>
#     '''

# @app.route("/transcription", methods=['POST'])
# def handle_transcription():
#     call_sid = request.form['CallSid']
#     transcript = request.form['TranscriptionText']
    
#     # Simple example of extracting information (you'd want more robust parsing)
#     name_match = re.search(r"My name is (\w+)", transcript)
#     phone_match = re.search(r"My phone number is (\d{10})", transcript)
    
#     name = name_match.group(1) if name_match else None
#     phone = phone_match.group(1) if phone_match else None
    
#     # Store in database
#     c.execute("INSERT INTO calls VALUES (?, ?, ?, ?)", (call_sid, transcript, name, phone))
#     conn.commit()
    
#     return "Transcription processed", 200
>>>>>>> 8588962 (good progress)

# if __name__ == "__main__":
#     app.run(debug=True)