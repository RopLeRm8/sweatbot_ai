import requests

def sendError(botIP: str):
    requests.post(
        "https://physions.com/botError",
        json={"botIP": botIP} 
    )

def finishBot(botIP: str, time: str):
    requests.post(
        "https://physions.com/finishBot",
        json={"botIP": botIP, "time": time} 
    )