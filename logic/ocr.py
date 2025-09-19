import pyautogui
from logic.paths import PATHS
import pytesseract
import time
import asyncio
from logic.api import sendError
from logic.discord import send_discord_log
import logic.config as config
from logic.utils import reset

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


async def wait_for_image(path, confidence=0.7, timeout=15, dontRestart = False, dontReport = False):
    start = time.time()
    while True:
        try:
            found = await asyncio.to_thread(pyautogui.locateOnScreen, path, confidence=confidence)
            if found:
                return found
        except pyautogui.ImageNotFoundException:
            pass

        if time.time() - start > timeout:
            if not dontRestart:
                send_discord_log(config.webhookURL, f"Couldn't identify image: {path}, bot restarts...")
                if not dontReport:
                    await sendError(config.json_config["self_ip"])
            return None
        await asyncio.sleep(0.5)


async def detect_error_detail() -> str | None:
    error_region = await wait_for_image(PATHS["failed_send"], confidence=0.9, timeout=5)
    if not error_region:
        return None

    left = error_region.left
    top = error_region.top
    width = error_region.width
    height = error_region.height

    ocr_region = (int(left), int(top + height), int(width) + 100, 40)

    screenshot = pyautogui.screenshot(region=ocr_region)
    text = pytesseract.image_to_string(screenshot, config='--psm 6').strip()

    return text

