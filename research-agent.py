import requests
import json
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("IBM_API_KEY")

# Get IAM token
token_response = requests.post(
    'https://iam.cloud.ibm.com/identity/token',
    data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
)
mltoken = token_response.json()["access_token"]

# API endpoint of your deployed Research Agent
endpoint_url = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8bd28700-8328-427d-ab54-8a6d851e1144/ai_service_stream?version=2021-05-01"

# Set prompt
user_input = "Summarize the latest research on renewable energy."

# Prepare request
payload = {
    "messages": [
        {
            "role": "user",
            "content": user_input
        }
    ]
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + mltoken
}

# Send request to Watsonx agent
response = requests.post(endpoint_url, json=payload, headers=headers)

# Show response
print("Agent Response:\n")
try:
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
    print(response.text)
