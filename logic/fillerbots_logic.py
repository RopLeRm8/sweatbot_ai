from logic.ocr import wait_for_image
from logic.paths import PATHS
import pyautogui
import asyncio

async def join_party():
    invite_accept = await wait_for_image(PATHS["invite_accept"], confidence=0.7, timeout=5)
    if invite_accept:
        pyautogui.click(invite_accept)
        await asyncio.sleep(0.5)
        pyautogui.click(invite_accept)
