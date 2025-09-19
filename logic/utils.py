import asyncio
from pydirectinput import press
from logic.ocr import wait_for_image
from logic.paths import PATHS
from logic.discord import send_discord_log
import logic.config as config

async def reset(max_attempts: int = 20):
    for _ in range(max_attempts):
        warzone = await wait_for_image(PATHS["warzone"], confidence=0.7, timeout=2, dontRestart=True)
        if warzone:
            return True 

        press("esc")
        await asyncio.sleep(1.5)

    send_discord_log(config.webhookURL, "Reset failed: Warzone menu not detected.")
    return False
