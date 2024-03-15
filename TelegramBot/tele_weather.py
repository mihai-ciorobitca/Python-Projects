from flask import Flask, request
import json
import os
from package import functions

# Get environment variables
CHAT_ID = os.getenv("ID")
TOKEN = os.getenv("TOKEN")
KEY = os.getenv("KEY")

# Initialize Flask app
app = Flask(__name__)

# Define a route for handling incoming POST requests to '/telebot'
@app.route('/telebot', methods=['POST'])
def webhook():
    # Parse the incoming JSON data from the Telegram API
    data = request.json
    
    # Extract relevant information from the incoming message
    if "message" in data:
        message_type = "message"
    else:
        message_type = "edited_message"
    chat_id = data[message_type]['chat']['id']
    message_text = data[message_type]['text']
    
    # Load user states from a JSON file
    with open('./user_states.json') as file:
        user_states = json.load(file)
    
    # Check if the received message is '/weather'
    if message_text == '/weather':
        # Respond to the user and set the user state to "city"
        response_text = "Write the city please"
        functions.send_message(chat_id, response_text)
        user_states[chat_id] = "city"
        
        # Save the updated user states to the JSON file
        with open('user_states.json', 'w') as file:
            json.dump(user_states, file)
    
    # Check if the user is in the "city" state
    elif str(chat_id) in user_states and user_states[str(chat_id)] == "city":
        # Get the weather for the provided city, respond, and reset user state
        response_text = functions.get_weather(message_text, KEY)
        functions.send_message(chat_id, response_text)
        del user_states[str(chat_id)]
        
        # Save the updated user states to the JSON file
        with open('user_states.json', 'w') as file:
            json.dump(user_states, file)
    
    # If the message is neither '/weather' nor in the "city" state, respond with an error message
    else:
        response_text = "Invalid option, check /help"
        functions.send_message(chat_id, response_text)

    # Return an empty response with status code 200
    return '', 200