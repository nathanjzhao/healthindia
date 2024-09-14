import logging
from flask import Flask, request, render_template, jsonify, Response, stream_with_context
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from dotenv import load_dotenv
import os
import requests
import time
from flask_cors import CORS  
from tts import text_to_speech
import json
from datetime import datetime

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
twilio_phone_number=os.getenv('TWILIO_PHONE_NUMBER')
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

# Add this to your global variables
conversation_history = {}

@app.route("/get_conversation", methods=['GET'])
def get_conversation():
    call_sid = request.args.get('call_sid')
    if call_sid in conversation_history:
        return jsonify(conversation_history[call_sid])
    return jsonify([])

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])  # Updated route to /login
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

            gather = Gather(input='speech', action=f'{ngrok_url}/handle_input', method='POST', speechTimeout=2)  # Updated action URL
            twiml.append(gather)

            call = client.calls.create(
                twiml=str(twiml),
                to=to_number,
                from_=twilio_phone_number
            )

            logger.info(f"Initiating call to {to_number}. Call SID: {call.sid}")
            return render_template('call-progress.html', call_sid=call.sid, to_number=to_number)
        except Exception as e:
            logger.error(f"Failed to create call: {str(e)}")
            return f"Failed to create call: {str(e)}", 500
    
    return render_template('login.html')

    # return '''
    #     <form method="post">
    #         Phone Number: <input type="text" name="to_number" id="to_number">
    #         <input type="submit" value="Call">
    #     </form>
    # '''

@app.route("/handle_input", methods=['POST'])
def handle_input():
    try:
        logger.info("handle_input called")
        
        user_input = request.form.get('SpeechResult')
        call_sid = request.form.get('CallSid')

        twiml = VoiceResponse()

        if not user_input:
            logger.warning("No speech input received")
            ai_response = "I'm sorry, I didn't catch that. Could you please repeat?"
        else:
            logger.info(f"User input: {user_input}")
            
            # Store user input in conversation history
            if call_sid not in conversation_history:
                conversation_history[call_sid] = []
            conversation_history[call_sid].append({"speaker": "user", "text": user_input})

            try:
                ai_response = generate_openai_response(user_input)
                logger.info(f"OpenAI response: {ai_response}")

                if ai_response:
                    if ai_response.lower() == "stop call":
                        ai_response = "Thank you for your time. Goodbye!"
                        twiml.say(ai_response)
                        twiml.hangup()
                    else:
                        s3_url = text_to_speech(ai_response)
                        if s3_url:
                            twiml.play(s3_url)
                        else:
                            ai_response = "I'm sorry, I couldn't generate the audio. Let's try again."
                            twiml.say(ai_response)
                else:
                    ai_response = "I'm sorry, I couldn't generate a response. Let's try again."
                    twiml.say(ai_response)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error calling OpenAI API: {str(e)}")
                ai_response = "I'm sorry, I'm having trouble thinking right now. Let's try again."
                twiml.say(ai_response)

            # Store AI response in conversation history
            conversation_history[call_sid].append({"speaker": "ai", "text": ai_response})

        # Always add a new Gather unless we're hanging up
        if 'hangup' not in twiml.verbs:
            gather = Gather(input='speech', action=f'{ngrok_url}/handle_input', method='POST', speechTimeout=2)
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

@app.route('/stream/<call_sid>')
def stream(call_sid):
    def event_stream():
        last_message_index = 0
        while True:
            if call_sid in conversation_history:
                current_messages = conversation_history[call_sid]
                if last_message_index < len(current_messages):
                    for message in current_messages[last_message_index:]:
                        yield f"data: {json.dumps(message)}\n\n"
                    last_message_index = len(current_messages)
            time.sleep(0.5)  # Check for new messages every 0.5 seconds

    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

# Path to the JSON file
JSON_CURR = 'user_history_+12223334444.json'
JSON_FILE = os.path.join(app.root_path, 'static', 'user_data', JSON_CURR)

# Utility to read the JSON file
def read_medical_record():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return {}

# Utility to write to the JSON file
def write_medical_record(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_entry_to_medical_record(new_entries):
    # Read the existing record
    record = read_medical_record()
    # Get the current time
    current_time = datetime.now().strftime("%m/%d/%Y %I:%M%") # Add the new entry using the current time as the key
    record['entries'].append({current_time: new_entries})
    # Write the updated record back to the JSON file
    write_medical_record(record)

@app.route('/medical-record', methods=['GET'])
def medical_record():
    # Read the medical record data from the JSON file
    record = read_medical_record()
    # Render the medical-record.html template and pass the record data
    return render_template('medical-record.html', record=record)

if __name__ == "__main__":
    app.run(debug=True)