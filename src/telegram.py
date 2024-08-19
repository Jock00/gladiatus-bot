import requests
from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN_TELEGRAM = os.getenv("BOT_TOKEN_TELEGRAM")


# The URL to get updates
url = f'https://api.telegram.org/bot{BOT_TOKEN_TELEGRAM}/getUpdates'

# Sending the request to get updates
response = requests.get(url)

# Checking the response
if response.status_code == 200:
    updates = response.json()
    print(updates)
else:
    print(f'Failed to get updates. Status code: {response.status_code}')
    print(f'Response: {response.text}')
