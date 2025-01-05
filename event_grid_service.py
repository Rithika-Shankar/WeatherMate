import requests
import json
from datetime import datetime

def publish_to_event_grid(disaster_data):
    topic_endpoint = "https://<your-topic-name>.<region>.eventgrid.azure.net/api/events"
    topic_key = "4FcyTcT64uRNzXsFLsokLYzBHpuwUUpzKGgfvGT5vqkfpLTlmlPJJQQJ99BAAC77bzfXJ3w3AAABAZEGUdF6"

    headers = {
        'Content-Type': 'application/json',
        'aeg-sas-key': topic_key,
    }

    event_data = [{
        "id": disaster_data['id'],
        "eventType": "DisasterReported",
        "subject": f"Disaster Reported: {disaster_data['eventName']}",
        "dataVersion": "1.0",
        "data": disaster_data,
        "eventTime": datetime.utcnow().isoformat()
    }]

    response = requests.post(topic_endpoint, headers=headers, json=event_data)
    
    if response.status_code == 200:
        print("Event successfully published to Event Grid!")
    else:
        print(f"Failed to publish event: {response.status_code}, {response.text}")
