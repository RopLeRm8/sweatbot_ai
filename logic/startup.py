import psutil
import time
import pyautogui
import os
import asyncio
from logic.discord import send_discord_log
from utils.schemas import StartRequest
import subprocess
from logic.game_flow import run_game_flow

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MENU_IMAGE_PATH = "../assets/menu_ready.png"
EXE_PATH = r"D:\SteamLibrary\steamapps\common\Call of Duty HQ\cod.exe"
COD_EXE_NAME = "cod.exe"

YES_PATH = os.path.join(BASE_DIR, "assets", "confirm.png")
CONTINUE_SETUP_PATH = os.path.join(BASE_DIR, "assets", "continue_setup.png")
MAIN_MENU_PATH = os.path.join(BASE_DIR, "assets", "main_menu.png")

DAY_PATH = os.path.join(BASE_DIR, "assets", "day.png")
MONTH_PATH = os.path.join(BASE_DIR, "assets", "month.png")
YEAR_PATH = os.path.join(BASE_DIR, "assets", "year.png")

FEBRUARY_PATH = os.path.join(BASE_DIR, "assets", "february.png")
TWO_PATH = os.path.join(BASE_DIR, "assets", "2.png")
YEARSCROLL_PATH = os.path.join(BASE_DIR, "assets", "2020.png")
YEARNUMBER_PATH = os.path.join(BASE_DIR, "assets", "2002.png")

CONFIRM_BIRTHDAY_PATH = os.path.join(BASE_DIR, "assets", "confirm_birthday.png")

CHECKBOX_PATH = os.path.join(BASE_DIR, "assets", "checkbox.png")
CONTINUE_PATH = os.path.join(BASE_DIR, "assets", "continue.png")


def handle_corrupted_patch_popup():
    try:
        yes_button = pyautogui.locateOnScreen(YES_PATH, confidence=0.7)
        if yes_button:
            pyautogui.click(yes_button)
    except pyautogui.ImageNotFoundException:
       pass

def handle_setup_continue():
    try:
        continue_button = pyautogui.locateOnScreen(CONTINUE_SETUP_PATH, confidence=0.7)
        if continue_button:
            pyautogui.click(continue_button)
            time.sleep(0.5)
            pyautogui.click(continue_button)
    except pyautogui.ImageNotFoundException:
       pass

def accept_legal_agreements():
    for _ in range(3):
        try:
            box = pyautogui.locateOnScreen(CHECKBOX_PATH, confidence=0.85)
            if box:
                pyautogui.click(box)
                time.sleep(0.5)
        except:
            pass

    for _ in range(10):
        try:
            cont_btn = pyautogui.locateOnScreen(CONTINUE_PATH, confidence=0.85)
            if cont_btn:
                pyautogui.click(cont_btn)
                time.sleep(0.5)
                pyautogui.click(cont_btn)
            time.sleep(1)
        except:
            pass

def is_cod_running():
    return any(proc.info["name"] == COD_EXE_NAME for proc in psutil.process_iter(attrs=["name"]))


# def handle_birthdate():
#     try:
#         day_button = pyautogui.locateOnScreen(DAY_PATH, confidence=0.85)
#         if day_button:
#             center = pyautogui.center(day_button)
#             pyautogui.click(center)
#             time.sleep(0.5)
#             pyautogui.click(center)
#             time.sleep(0.5)
#             dayToSelect = pyautogui.locateOnScreen(TWO_PATH, confidence=0.85)
#             if dayToSelect:
#                 pyautogui.click(dayToSelect)
#                 time.sleep(1)
#     except pyautogui.ImageNotFoundException:
#        pass

#     try:
#         month_button = pyautogui.locateOnScreen(MONTH_PATH, confidence=0.85)
#         if month_button:
#             center = pyautogui.center(month_button)
#             pyautogui.click(center)
#             time.sleep(0.5)
#             pyautogui.click(center)
#             time.sleep(0.5)
#             monthToSelect = pyautogui.locateOnScreen(FEBRUARY_PATH, confidence=0.85)
#             if monthToSelect:
#                 pyautogui.click(monthToSelect)
#                 time.sleep(1)
#     except pyautogui.ImageNotFoundException:
#        pass
#     try:
#         year_button = pyautogui.locateOnScreen(YEAR_PATH, confidence=0.85)
#         if year_button:
#             center = pyautogui.center(year_button)
#             pyautogui.click(center)
#             time.sleep(0.5)
#             pyautogui.click(center)
#             time.sleep(0.5)
#             yearToScroll = pyautogui.locateOnScreen(YEARSCROLL_PATH, confidence=0.85)
#             if yearToScroll:
#                 pyautogui.moveTo(yearToScroll)
#                 time.sleep(0.25)
#                 pyautogui.scroll(-300)
#                 yearToSelect = pyautogui.locateOnScreen(YEARNUMBER_PATH, confidence=0.95)
#                 center = pyautogui.center(yearToSelect)
#                 pyautogui.click(center)
#                 time.sleep(0.5)
#                 pyautogui.click(center)
#                 time.sleep(1)
#     except pyautogui.ImageNotFoundException:
#        pass
    
#     try:
#         continue_button = pyautogui.locateOnScreen(CONTINUE_SETUP_PATH, confidence=0.85)
#         if continue_button:
#             pyautogui.click(continue_button)
#             time.sleep(0.5)
#             pyautogui.click(continue_button)
#     except pyautogui.ImageNotFoundException:
#        pass

#     try:
#         confirm_birthday = pyautogui.locateOnScreen(CONFIRM_BIRTHDAY_PATH, confidence=0.85)
#         if confirm_birthday:
#             pyautogui.click(confirm_birthday)
#             time.sleep(0.5)
#             pyautogui.click(confirm_birthday)
#     except pyautogui.ImageNotFoundException:
#        pass

    


async def launch_cod(payload: StartRequest):
    send_discord_log(payload.webhookURL, "Initializing bot instance.")
    if not is_cod_running():
        send_discord_log(payload.webhookURL, "COD not running, initializing on bot instance.")

        subprocess.Popen(
            [
                r"C:\Program Files (x86)\Steam\steam.exe",
                "-applaunch",
                "1938090"
            ]
        )
        await wait_for_cod_menu(payload,1800)
        return
    send_discord_log(payload.webhookURL, "Bot loaded successfully. Attempting to invite user: {}".format(payload.activision_id))
    await run_game_flow(payload)

    


async def wait_for_cod_menu(payload: StartRequest, timeout=120):
    start_time = time.time()
    while True:
        try:
            await asyncio.to_thread(handle_corrupted_patch_popup)
            await asyncio.to_thread(accept_legal_agreements)
            await asyncio.to_thread(handle_setup_continue)
            # await asyncio.to_thread(handle_birthdate)

            found = await asyncio.to_thread(
                pyautogui.locateOnScreen,
                MAIN_MENU_PATH,
                confidence=0.8
            )

            if found:
                send_discord_log(payload.webhookURL, "Bot loaded succesfully, inviting the {}".format(payload.activision_id))
                await run_game_flow(payload)
 
                break

            if time.time() - start_time > timeout:
                send_discord_log(payload.webhookURL, "Bot has timed out while loading into COD, please investigate.")
                raise TimeoutError("Timed out waiting for main menu.")

        except asyncio.CancelledError:
            print("Loop cancelled gracefully.")
            exit(0) 
        except KeyboardInterrupt:
            exit(0)
        except pyautogui.ImageNotFoundException:
            pass

        await asyncio.sleep(1)