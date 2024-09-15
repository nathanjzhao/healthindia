from datetime import datetime
import logging
from flask import Flask, redirect, request, render_template, jsonify, Response, stream_with_context, session, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time
from flask_cors import CORS  
from tts import text_to_speech
import json
from user_history import finalize_call, load_user_history, save_user_history, update_user_info, finalize_call, add_entry_to_history
from conversation_logic import interpret_response, update_user_history, rephrase_question
from tree import decisionTree

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app) 

# Load environment variables
load_dotenv()

# Twilio and OpenAI credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
twilio_phone_number=os.getenv('TWILIO_PHONE_NUMBER')
ngrok_url = os.getenv('NGROK_URL')

# Twilio client
client = Client(account_sid, auth_token)

# Global variables
predictionState = "root"
conversation_history = {}

language_mappings = {
    'en': {
        'welcome': "Hello, welcome to the AI-assisted medical diagnosis.",
        'welcome_back': "Hello {}, welcome back to the AI-assisted medical diagnosis.",
        'didnt_catch': "I'm sorry, I didn't catch that. Could you please repeat?",
        'couldnt_understand': "I couldn't understand your response.",
        'consult_professional': "Based on your answers, you may have {}. Please consult a medical professional for proper diagnosis.",
        'thank_you': "Thank you for your time. Goodbye!",
        'error_processing': "I'm sorry, I'm having trouble processing your response. Let's try again.",
        'error_occurred': "I'm sorry, an error occurred. Please try again later.",
        'gather_language': 'en-US'
    },
    'hi': {
        'welcome': "नमस्ते, AI-सहायता प्राप्त चिकित्सा निदान में आपका स्वागत है।",
        'welcome_back': "नमस्ते {}, AI-सहायता प्राप्त चिकित्सा निदान में आपका फिर से स्वागत है।",
        'didnt_catch': "क्षमा करें, मुझे वह समझ नहीं आया। कृपया दोहराएं?",
        'couldnt_understand': "मैं आपके जवाब को समझ नहीं पाया।",
        'consult_professional': "आपके जवाबों के आधार पर, आपको {} हो सकता है। कृपया उचित निदान के लिए चिकित्सा पेशेवर से परामर्श करें।",
        'thank_you': "आपके समय के लिए धन्यवाद। अलविदा!",
        'error_processing': "क्षमा करें, मुझे आपके जवाब को संसाधित करने में समस्या हो रही है। फिर से प्रयास करें।",
        'error_occurred': "क्षमा करें, एक त्रुटि हुई। कृपया बाद में पुनः प्रयास करें।",
        'gather_language': 'hi-IN'
    },
    'ta': {
    'welcome': "வணக்கம், AI உதவியுடன் மருத்துவ பரிசோதனைக்கு உங்களை வரவேற்கிறோம்.",
    'welcome_back': "வணக்கம் {}, AI உதவியுடன் மருத்துவ பரிசோதனைக்கு உங்களை மீண்டும் வரவேற்கிறோம்.",
    'didnt_catch': "மன்னிக்கவும், எனக்கு அது புரியவில்லை. தயவுசெய்து மீண்டும் கூறுங்கள்?",
    'couldnt_understand': "உங்கள் பதில் எனக்கு புரியவில்லை.",
    'consult_professional': "உங்கள் பதில்களின் அடிப்படையில், உங்களுக்கு {} இருக்கக்கூடும். சரியான பரிசோதனைக்கு மருத்துவரின் ஆலோசனை பெறவும்.",
    'thank_you': "உங்கள் நேரத்திற்கு நன்றி. வணக்கம்!",
    'error_processing': "மன்னிக்கவும், உங்கள் பதிலை செயலாக்க முயற்சிக்கும்போது சிக்கல் ஏற்பட்டது. மீண்டும் முயல்கின்றேன்.",
    'error_occurred': "மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது. பிறகு மீண்டும் முயற்சிக்கவும்.",
    'gather_language': 'ta-IN'
    }
}

@app.route("/get_conversation", methods=['GET'])
def get_conversation():
    global conversation_history 
    call_sid = request.args.get('call_sid')
    if call_sid in conversation_history:
        return jsonify(conversation_history[call_sid])
    return jsonify([])

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    language = session.get('language', 'en')
    global predictionState, conversation_history
    if request.method == 'POST':
        to_number = request.form['to_number']
        to_number = ''.join(filter(str.isdigit, to_number))
        
        if len(to_number) == 10:
            to_number = f"+1{to_number}"
        
        if not to_number.startswith('+') or not to_number[1:].isdigit():
            return "Invalid phone number format. Please use E.164 format.", 400
        
        contact_method = request.form.get('contact_method', 'call')  # Default to 'call' if not provided
        
        try:
            user_history = load_user_history(to_number)
            
            if contact_method == 'call':
                twiml = VoiceResponse()
                predictionState = "root"
                root_question = decisionTree["root"]["question"]

                if user_history["fname"]:
                    speech_text = language_mappings[language]['welcome_back'].format(user_history['fname']) + " " + root_question
                else:
                    speech_text = language_mappings[language]['welcome'] + " " + root_question

                # Generate speech file and get S3 URL
                s3_url = text_to_speech(speech_text, language)
                if s3_url:
                    print(f"Audio data URL: {s3_url[:100]}...")
                    twiml.play(s3_url)
                else:
                    twiml.say("I'm sorry, I couldn't generate the audio. Let's try again.")

                gather = Gather(input='speech', language=language_mappings[language]['gather_language'], action=f'{ngrok_url}/handle_input', method='POST', speechTimeout=1)
                twiml.append(gather)

                call = client.calls.create(
                    twiml=str(twiml),
                    to=to_number,
                    from_=twilio_phone_number
                )

                # Add the first message to conversation history
                if call.sid not in conversation_history:
                    conversation_history[call.sid] = []
                conversation_history[call.sid].append({"speaker": "ai", "text": speech_text})

                logger.info(f"Initiating call to {to_number}. Call SID: {call.sid}")
                return render_template('call-progress.html', call_sid=call.sid, to_number=to_number)
            elif contact_method == 'text':
                logger.info(f"Initiating text conversation with {to_number}")
                
                # Send initial text message
                message = client.messages.create(
                    body=language_mappings[language]['welcome'],
                    from_=twilio_phone_number,
                    to=to_number
                )
                
                # Add the first message to conversation history
                if message.sid not in conversation_history:
                    conversation_history[message.sid] = []
                conversation_history[message.sid].append({"speaker": "ai", "text": language_mappings[language]['welcome']})
                
                logger.info(f"Initiating text conversation with {to_number}. Message SID: {message.sid}")
                return render_template('text-conversation.html', message_sid=message.sid, to_number=to_number)
        except Exception as e:
            logger.error(f"Failed to initiate contact: {str(e)}")
            return f"Failed to initiate contact: {str(e)}", 500
    
    return render_template('login.html')

@app.route("/sms", methods=['POST'])
def handle_sms():
    language = session.get('language', 'en')
    global predictionState, conversation_history
    
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    user_history = load_user_history(from_number)
    
    # Process the incoming message using the same conversation logic
    try:
        current_node = decisionTree[predictionState]
        current_question = current_node["question"]
        interpreted_response = interpret_response(incoming_msg, current_node)
        
        new_user_history = update_user_history(current_question, incoming_msg, user_history)
        
        if interpreted_response == "invalid":
            ai_response = rephrase_question(current_question, incoming_msg, True, new_user_history)
        else:
            if interpreted_response in current_node:
                predictionState = current_node[interpreted_response]
            else:
                ai_response = f"{language_mappings[language]['couldnt_understand']} {current_question}"
            
            if predictionState not in decisionTree:
                ai_response = language_mappings[language]['consult_professional'].format(predictionState)
                finalize_call(user_history)
            else:
                next_question = decisionTree[predictionState]["question"]
                ai_response = rephrase_question(next_question, incoming_msg, False, user_history)
        
        save_user_history(from_number, user_history)
        
        # Send the response back via SMS
        resp = MessagingResponse()
        resp.message(ai_response)
        
        return str(resp)
    
    except Exception as e:
        logger.error(f"Error processing SMS: {str(e)}")
        resp = MessagingResponse()
        resp.message(language_mappings[language]['error_occurred'])
        return str(resp)

@app.route("/handle_input", methods=['POST'])
def handle_input():
    language = session.get('language', 'en')
    global predictionState, conversation_history
    try:
        logger.info("handle_input called")
        
        user_input = request.form.get('SpeechResult')
        call_sid = request.form.get('CallSid')
        to_number = request.form.get('To')

        twiml = VoiceResponse()

        if not user_input:
            logger.warning("No speech input received")
            ai_response = language_mappings[language]['didnt_catch']
        else:
            logger.info(f"User input: {user_input}")
            
            user_history = load_user_history(to_number)
            
            # Store user input in conversation history
            if call_sid not in conversation_history:
                conversation_history[call_sid] = []
            conversation_history[call_sid].append({"speaker": "user", "text": user_input})

            try:
                current_node = decisionTree[predictionState]
                current_question = current_node["question"]
                interpreted_response = interpret_response(user_input, current_node)
                
                # Still update user information if doesn't answer question
                new_user_history = update_user_history(current_question, user_input, user_history)
                if interpreted_response == "invalid":
                    ai_response = rephrase_question(current_question, user_input, True, new_user_history)
                else:
                    if interpreted_response in current_node:
                        predictionState = current_node[interpreted_response]
                    else:
                        ai_response = f"{language_mappings[language]['couldnt_understand']} {current_question}"
                    
                    if predictionState not in decisionTree:
                        ai_response = language_mappings[language]['consult_professional'].format(predictionState)
                        finalize_call(user_history)
                    else:
                        next_question = decisionTree[predictionState]["question"]
                        ai_response = rephrase_question(next_question, user_input, False, user_history)

                logger.info(f"AI response: {ai_response}")

                if ai_response.lower() == "stop call":
                    finalize_call(user_history)
                    ai_response = language_mappings[language]['thank_you']
                    twiml.say(ai_response)
                    twiml.hangup()
                else:
                    s3_url = text_to_speech(ai_response, language)
                    if s3_url:
                        twiml.play(s3_url)
                    else:
                        twiml.say(ai_response)
                
                save_user_history(to_number, user_history)
                print("user_history: ", user_history)
            except Exception as e:
                logger.error(f"Error processing input: {str(e)}")
                ai_response = language_mappings[language]['error_processing']
                twiml.say(ai_response)

                finalize_call(user_history)

            # Store AI response in conversation history
            conversation_history[call_sid].append({"speaker": "ai", "text": ai_response})

        # Always add a new Gather unless we're hanging up
        if 'hangup' not in twiml.verbs:
            gather = Gather(input='speech', language=language_mappings[language]['gather_language'], action=f'{ngrok_url}/handle_input', method='POST', speechTimeout=1)
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
        error_message = language_mappings[language]['error_occurred']
        twiml.say(error_message)
        
        # Send a text message to continue the conversation
        client.messages.create(
            body=f"{error_message} The call has been disconnected due to unknown issues. Please text this number to continue the conversation.",
            from_=twilio_phone_number,
            to=to_number
        )
        
        return str(twiml), 500

@app.route('/stream/<call_sid>')
def stream(call_sid):
    global conversation_history
    def event_stream():
        last_message_index = 0
        while True:
            if call_sid in conversation_history:
                current_messages = conversation_history[call_sid]
                if last_message_index < len(current_messages):
                    for message in current_messages[last_message_index:]:
                        yield f"data: {json.dumps(message)}\n\n"
                    last_message_index = len(current_messages)
            time.sleep(0.5)

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
    current_time = datetime.now().strftime("%m/%d/%Y %I:%M%p")
    # Add the new entry using the current time as the key
    record['entries'].append({current_time: new_entries})
    # Write the updated record back to the JSON file
    write_medical_record(record)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Get form data
    phone_number = request.form['phone_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    gender = request.form['gender']
    height = request.form['height']
    weight = request.form['weight']
    reason = request.form['reason']

    # Load or create user history
    user_history = load_user_history(phone_number)

    # Update user information
    update_user_info(user_history, 'fname', first_name)
    update_user_info(user_history, 'lname', last_name)
    update_user_info(user_history, 'age',  age)  # Convert DOB to age
    update_user_info(user_history, 'gender', gender)
    update_user_info(user_history, 'height', height)
    update_user_info(user_history, 'weight', weight)

    # Add the reason for visit to the current call information
    add_entry_to_history(user_history, [f"Reason for visit: {reason}"])

    # Save the updated user history
    finalize_call(user_history)
    save_user_history(phone_number, user_history)

    # Redirect to the medical record page to display the updated data
    return redirect(url_for('medical_record', phone_number=phone_number))

@app.route('/medical-record/<phone_number>')
def medical_record(phone_number):
    # Load the user history to display
    user_history = load_user_history(phone_number)
    return render_template('medical-record.html', record=user_history)

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language')
    session['language'] = language
    return redirect(url_for('login'))

@app.route('/webform')
def webform():
    return render_template('webform.html')

if __name__ == "__main__":
    app.run(debug=True)