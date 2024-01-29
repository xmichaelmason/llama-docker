from flask import render_template, request, jsonify
from openai import OpenAI
from lib.openai_client import ChatAssistant
import os

openai_instance = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))
chat_assistant = ChatAssistant(openai_instance)

def index():
    return render_template('index.html')

def chat():
    message = request.form['message']

    # Retrieve Freshservice results based on the incoming message

    # Add user message to ChatAssistant
    chat_assistant.add_message("user", message)

    # Generate a response using the ChatAssistant instance
    response = chat_assistant.generate_response()

    # Check if the response is a string
    if isinstance(response, str):
        # Add response message to ChatAssistant
        chat_assistant.add_message("assistant", response)
    else:
        # Handle the error when the response is not a string
        # You can log the error or display an error message to the user
        print("Error: Invalid response format")

    return jsonify({'message': response})

def clear_messages():
    chat_assistant.clear_messages()
    chat_assistant.save_messages()
    return jsonify({'message': 'Messages cleared'})