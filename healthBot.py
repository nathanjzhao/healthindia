import os
import openai
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load and preprocess data
training = pd.read_csv('Training.csv')
testing = pd.read_csv('Testing.csv')

cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

# Train the decision tree classifier
clf = DecisionTreeClassifier()
clf = clf.fit(x, y)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    user_info = data.get('userInfo')

    # Call the function from healthBot.py to process the user's message
    response_text = handle_chat(user_message, user_info)
    return jsonify({"response": response_text})


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    symptoms = data['symptoms']
    diagnosis = tree_to_code(clf, cols, symptoms)
    return jsonify({'diagnosis': diagnosis})

def chatgpt_prompt(question, system_message="You are a helpful health assistant interacting with a health diagnosis bot called 'MedBot'."):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "I couldn't process your request. Please try again."
def handle_chat(user_message, user_info):
    # Your logic to process the user message and information
    # For example, generate a response based on the input
    age = user_info.get('age')
    height = user_info.get('height')
    weight = user_info.get('weight')
    date = user_info.get('date')

    # Generate a simple response (you can replace this with more complex logic)
    response_text = f"Received your message: {user_message}. Your info - Age: {age}, Height: {height} cm, Weight: {weight} kg, Date: {date}."
    
    return response_text


def tree_to_code(tree, feature_names, symptoms):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    
    def recurse(node, depth):
        if tree_.feature[node] != tree.TREE_UNDEFINED:
            name = feature_name[node]
            if name in symptoms:
                return recurse(tree_.children_right[node], depth + 1)
            else:
                return recurse(tree_.children_left[node], depth + 1)
        else:
            return le.inverse_transform(tree_.value[node].argmax(axis=1))[0]
    
    return recurse(0, 1)

if __name__ == '__main__':
    # Ensure the API key is set in the environment before running
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    app.run(debug=True)
