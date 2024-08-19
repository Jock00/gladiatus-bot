import requests

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
BOT_TOKEN = '7290063693:AAH18br8EGmdjScereqPCOSmzRFWr6wQVVw'

# The URL to get updates
url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'

# Sending the request to get updates
response = requests.get(url)

# Checking the response
if response.status_code == 200:
    updates = response.json()
    print(updates)
else:
    print(f'Failed to get updates. Status code: {response.status_code}')
    print(f'Response: {response.text}')
