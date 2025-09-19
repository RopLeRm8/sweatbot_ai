import requests
from logic.utils import reset

async def sendError(botIP: str):
    requests.post(
        "https://physions.com/botError",
        json={"botIP": botIP} 
    )
    await reset()

def finishBot(botIP: str, time: str):
    requests.post(
        "https://physions.com/finishBot",
        json={"botIP": botIP, "time": time} 
    )
    