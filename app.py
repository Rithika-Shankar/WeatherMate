import pandas as pd
from flask import Flask, render_template, request, jsonify
import requests
from event_grid_service import publish_to_event_grid

app = Flask(__name__)

# Azure OpenAI GPT Model URL and API Key
OPENAI_URL = "https://rithi-m5j5mp5d-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
OPENAI_API_KEY = "5WIdIHrYBm3QKZ3Xvcz7OsCOPBJkvSHw6j1JMqEl7Ava21wRBL8gJQQJ99BAACHYHv6XJ3w3AAAAACOG0Wnh"

# Weather API Key
weather_api_key = '4105e115781bcc407e5980d20cd0d5d6'

# Load disaster data from CSV file
def load_disaster_data():
    df = pd.read_csv('disaster.csv')  # Ensure the file is in the same directory
    return df

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    map_center = [77.5946, 12.9716]  # Default to Bengaluru coordinates
    disaster_data = load_disaster_data()
    
    if request.method == 'POST':
        location = request.form['location']
        weather_data = get_weather_alerts(weather_api_key, location)
        if weather_data:
            map_center = [weather_data['coord']['lon'], weather_data['coord']['lat']]
    
    # Convert the disaster data to a dictionary format for easy access in the front-end
    disaster_data_dict = disaster_data.to_dict(orient='records')
    
    return render_template('index.html', weather_data=weather_data, map_center=map_center, disaster_data=disaster_data_dict)

def get_weather_alerts(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/disaster-report', methods=['POST'])
def disaster_report():
    disaster_data = request.json
    try:
        publish_to_event_grid(disaster_data)
        return "Disaster report received and event published", 200
    except Exception as e:
        return f"Error publishing event: {str(e)}", 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Check for predefined questions related to disaster or weather
    predefined_responses = {
        "How can I prepare for an earthquake?": "Make sure you have an emergency kit, know evacuation routes, and secure heavy furniture.",
        "What should I do during a flood warning?": "Stay indoors, move to higher ground, and avoid driving on flooded roads."
    }

    # If user input matches predefined questions, return the respective response
    if user_input in predefined_responses:
        return jsonify({"reply": predefined_responses[user_input]}), 200

    # Otherwise, use OpenAI model for generic responses
    headers = {
        'Content-Type': 'application/json',
        'api-key': OPENAI_API_KEY
    }
    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 150
    }

    try:
        response = requests.post(OPENAI_URL, headers=headers, json=payload)
        response_data = response.json()
        gpt_reply = response_data['choices'][0]['message']['content']
        return jsonify({"reply": gpt_reply}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
