from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import sqlite3
import re
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('calls.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS calls
             (call_sid TEXT, transcript TEXT, name TEXT, phone TEXT)''')
conn.commit()

@app.route("/", methods=['GET', 'POST'])
def voice():
    if request.method == 'POST':
        to_number = request.form['to_number']
        
        # Clean the phone number input
        to_number = re.sub(r'[^\d]', '', to_number)  # Remove non-digit characters
        
        # Convert to E.164 format if necessary
        if len(to_number) == 10 and to_number.isdigit():
            to_number = f"+1{to_number}"  # Assuming US country code
        
        # Validate phone number format
        if not re.match(r'^\+\d{1,15}$', to_number):
            return "Invalid phone number format. Please use E.164 format.", 400
        
        # Twilio credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        print(account_sid, to_number, auth_token, os.getenv('TWILIO_PHONE_NUMBER'))
        
        try:
            call = client.calls.create(
                to=to_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url='https://a903-192-12-14-0.ngrok-free.app/'  # URL to handle the call
            )
            return f"Calling {to_number}..."
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
                var regex = /^\+?\d{10,15}$/;  // E.164 format
                if (!regex.test(phoneNumber)) {
                    alert("Invalid phone number format. Please use E.164 format.");
                    return false;  // Prevent form submission
                }
                return true;  // Allow form submission
            }
        </script>
    '''

@app.route("/transcription", methods=['POST'])
def handle_transcription():
    call_sid = request.form['CallSid']
    transcript = request.form['TranscriptionText']
    
    # Simple example of extracting information (you'd want more robust parsing)
    name_match = re.search(r"My name is (\w+)", transcript)
    phone_match = re.search(r"My phone number is (\d{10})", transcript)
    
    name = name_match.group(1) if name_match else None
    phone = phone_match.group(1) if phone_match else None
    
    # Store in database
    c.execute("INSERT INTO calls VALUES (?, ?, ?, ?)", (call_sid, transcript, name, phone))
    conn.commit()
    
    return "Transcription processed", 200

if __name__ == "__main__":
    app.run(debug=True)