import requests

def send_discord_log(webhookURL: str, message:str):
    payload = {
        "embeds": [
            {
                "title": "🤖 PHYSION-01 Process Log",
                "description": message,
                "color": 8900331 
            }
        ]
    }
    response = requests.post(webhookURL, json=payload)
    if  response.status_code != 204:
        print("Failed to send log")
