from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import re
import urllib.parse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Use an absolute path for CALLS_FILE
CALLS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calls.json')

def load_calls():
    try:
        if Path(CALLS_FILE).exists():
            with open(CALLS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading calls: {e}")
    return {}

def save_calls(calls):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(CALLS_FILE), exist_ok=True)
        with open(CALLS_FILE, 'w') as f:
            json.dump(calls, f, indent=2)
        logging.info(f"Calls saved to {CALLS_FILE}")
    except Exception as e:
        logging.error(f"Error saving calls: {e}")

@app.route("/", methods=['GET', 'POST'])
def voice():
    if request.method == 'POST':
        to_number = request.form['to_number']
        to_number = re.sub(r'[^\d]', '', to_number)
        
        if len(to_number) == 10 and to_number.isdigit():
            to_number = f"+1{to_number}"
        
        if not re.match(r'^\+\d{1,15}$', to_number):
            return "Invalid phone number format. Please use E.164 format.", 400
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        
        try:
            base_url = request.url_root.rstrip('/')
            twiml = f"""
            <Response>
                <Say>Hello, this is a test call. Please say your name.</Say>
                <Record maxLength="10" transcribe="true" transcribeCallback="{base_url}/transcribe_name"/>
                <Say>Now, please say your phone number.</Say>
                <Record maxLength="15" transcribe="true" transcribeCallback="{base_url}/transcribe_phone"/>
                <Say>Thank you for providing your information. Goodbye!</Say>
            </Response>
            """
            
            call = client.calls.create(
                twiml=twiml,
                to=to_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER')
            )
            return f"Calling {to_number}... Call SID: {call.sid}"
        except Exception as e:
            return f"Failed to create call: {str(e)}", 500
    
    return '''
        <form method="post" onsubmit="return validatePhoneNumber()">
            Phone Number: <input type="text" name="to_number" id="to_number">
            <input type="submit" value="Call">
        </form>
        <script>
            function validatePhoneNumber() {
                var phoneNumber = document.getElementById('to_number').value;
                var regex = /^\+?\d{10,15}$/;
                if (!regex.test(phoneNumber)) {
                    alert("Invalid phone number format. Please use E.164 format.");
                    return false;
                }
                return true;
            }
        </script>
    '''

@app.route("/transcribe_name", methods=['POST'])
def transcribe_name():
    call_sid = request.form['CallSid']
    transcript = request.form['TranscriptionText']

    logging.info(f"Name transcription for call {call_sid}: {transcript}")
    
    calls = load_calls()
    calls[call_sid] = {'name': transcript}
    save_calls(calls)
    
    return "Name transcription processed", 200

@app.route("/transcribe_phone", methods=['POST'])
def transcribe_phone():
    call_sid = request.form['CallSid']
    transcript = request.form['TranscriptionText']
      
    calls = load_calls()
    logging.info(f"Phone transcription for call {call_sid}: {transcript}")
    if call_sid in calls:
        calls[call_sid]['phone'] = transcript
    else:
        calls[call_sid] = {'phone': transcript}
    save_calls(calls)
    
    return "Phone transcription processed", 200

if __name__ == "__main__":
    app.run(debug=True)