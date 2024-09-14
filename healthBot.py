import os
import openai
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier

# Load and preprocess the training data
try:
    training = pd.read_csv('data/Training.csv')
    cols = training.columns[:-1]
    x = training[cols]
    y = training['prognosis']

    le = preprocessing.LabelEncoder()
    le.fit(y)
    y_encoded = le.transform(y)

    clf = DecisionTreeClassifier().fit(x, y_encoded)
except Exception as e:
    print(f"Error loading and processing training data: {str(e)}")  # Debugging line

# Set OpenAI API key (make sure it's correctly set up)
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_symptoms(message, symptom_list):
    symptoms_mentioned = []
    for symptom in symptom_list:
        if symptom.lower() in message.lower():
            symptoms_mentioned.append(symptom)
    return symptoms_mentioned

def handle_chat(user_message, user_info, history):
    try:
        print(f"User message: {user_message}")  # Debugging line
        print(f"User info: {user_info}")        # Debugging line
        print(f"History: {history}")            # Debugging line

        symptom_list = cols.tolist()
        symptoms_mentioned = extract_symptoms(user_message, symptom_list)

        collected_symptoms = user_info.get('symptoms', [])
        collected_symptoms.extend(symptoms_mentioned)
        collected_symptoms = list(set(collected_symptoms))
        user_info['symptoms'] = collected_symptoms

        messages = [
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": f"User info: {user_info}"},
            {"role": "user", "content": user_message}
        ]
        messages.extend(history)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        assistant_message = response['choices'][0]['message']['content'].strip()

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})

        return {
            "response": assistant_message,
            "userInfo": user_info,
            "history": history
        }

    except Exception as e:
        print(f"Error in handle_chat: {str(e)}")  # Debugging line
        raise
