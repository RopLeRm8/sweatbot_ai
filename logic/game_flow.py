import time
import pyautogui
import asyncio
from utils.schemas import StartRequest
from pydirectinput import press, keyDown, keyUp
from logic.discord import send_discord_log
from logic.ocr import detect_error_detail, wait_for_image
from logic.paths import PATHS
from logic.api import sendError,finishBot
import logic.config as config
from logic.utils import reset
import requests
import aiohttp
import time

start_time = None

def type_string(text: str):
    for char in text:
        if char.isupper():
            pyautogui.keyDown('shift')
            pyautogui.press(char.lower())
            pyautogui.keyUp('shift')

        elif char == ' ':
            pyautogui.press('space')

        elif char == '#': 
            pyautogui.keyDown('alt')  
            pyautogui.keyDown('ctrl') 
            pyautogui.press('3')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('alt')

        elif char.isalnum():
            pyautogui.press(char)

        else:
            pyautogui.typewrite(char)
        time.sleep(0.1)

def type_string(text: str): 
    for char in text: 
        if char.isupper(): 
            keyDown('shift')
            press(char.lower()) 
            keyUp('shift') 
        elif char == ' ': 
            press('space') 
        elif char == '#': 
            keyDown('shift') 
            press('3') 
            keyUp('shift') 
        elif char.isalnum(): 
            press(char) 
        time.sleep(0.1)

async def notify_bots(bots, webhook_url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for bot in bots:
            url = f"{bot['ip']}/bot_leave"
            tasks.append(session.post(url, json={"webhookURL": webhook_url}))
        await asyncio.gather(*tasks, return_exceptions=True)
        
async def leaveGame(isLeader: bool):
    if not isLeader:
        press("esc")
        await asyncio.sleep(5)
        press("esc")
        await asyncio.sleep(3)

    leave_match = await wait_for_image(PATHS["leave"], confidence=0.7, timeout=25, dontRestart=not isLeader, dontReport=isLeader)

    # if isLeader:
    #         bots = config.json_config["followers"]
    #         asyncio.create_task(notify_bots(bots, config.webhookURL))

    pyautogui.click(leave_match)

    if not isLeader:
        leave_match_confirm = await wait_for_image(PATHS["leave_confirm_notleader"], confidence=0.7, timeout=25, dontReport=True)
    else:
        leave_match_confirm = await wait_for_image(PATHS["leave_confirm"], confidence=0.7, timeout=25)

    await asyncio.sleep(5)
    pyautogui.moveTo(leave_match_confirm)
    await asyncio.sleep(1)
    pyautogui.click(leave_match_confirm)
    await asyncio.sleep(10)
    press("esc")
    await asyncio.sleep(2)

    if isLeader:
        global start_time
        elapsed = time.monotonic() - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        timeElapsed = f"{minutes} minutes {seconds} seconds"
        start_time = None
        finishBot(config.json_config["self_ip"], timeElapsed)


async def verifyPreLobby(webhookURL: str):
    await asyncio.sleep(10)
    timeout = 300

    while True:
        found = await wait_for_image(PATHS["loadouts"], confidence=0.7, timeout=2, dontRestart=True)
        if found:
            send_discord_log(webhookURL, "Match Found. Returning back to the lobby & refreshing.\nThank you for using SweatProof.")
            press("esc")
            await asyncio.sleep(5)
            press("esc")
            await leaveGame(isLeader=True)
            break  

        timeout -= 5
        if timeout <= 0:
            send_discord_log(webhookURL, "Bot instance didn't load into the match on time, session cancelled.")
            sendError(config.json_config["self_ip"])
            break


async def verifyIfSearching(webhookURL: str):
    await asyncio.sleep(1)

    while (True):
        await asyncio.sleep(2)
        searching = await wait_for_image(PATHS["searching"], confidence=0.7, timeout=2, dontRestart=True)
        if searching:
            send_discord_log(webhookURL, "Queue started.")
            break
        cancel_button =  await wait_for_image(PATHS["cancel_search"], confidence=0.7, timeout=6)
        pyautogui.moveTo(cancel_button)
        await asyncio.sleep(1)
        pyautogui.click(cancel_button)
        await asyncio.sleep(1)
        confirm_cancel = await wait_for_image(PATHS["confirm_cancel_search"], confidence=0.7, timeout=6)
        pyautogui.moveTo(confirm_cancel)
        await asyncio.sleep(1)
        pyautogui.click(confirm_cancel)


        queue = await wait_for_image(PATHS["queue"], confidence=0.7, timeout=15)
        pyautogui.moveTo(queue)
        await asyncio.sleep(1)
        pyautogui.click(queue)
        send_discord_log(webhookURL, 'Game is experiencing "Connecting Bug", restarting the queueing system.')

async def selectWarzone():
    warzone_button = await wait_for_image(PATHS["warzone"], confidence=0.7)
    if warzone_button:
        pyautogui.click(warzone_button)
        time.sleep(0.5)
        pyautogui.click(warzone_button)
        time.sleep(7)

async def setPartyInviteOnly():
    press("o")
    await asyncio.sleep(2.5)

    settings_button = await wait_for_image(PATHS["party_settings"], confidence=0.7)
    if not settings_button: return

    pyautogui.click(settings_button)
    await asyncio.sleep(2)

    invite_only = await wait_for_image(PATHS["invite_only"], confidence=0.7)
    if not invite_only: return

    pyautogui.click(invite_only)
    time.sleep(0.5)
    pyautogui.click(invite_only)
    await asyncio.sleep(2)


    press("esc")
    time.sleep(1)
    press("esc")
    await asyncio.sleep(2)


async def inviteToParty(webhookURL : str, botId : str | None = None, botIP: str | None = None):
    await asyncio.sleep(2)
    player_select = await wait_for_image(PATHS["player_select"], confidence=0.7)

    x = player_select.left + player_select.width // 2
    y = player_select.top + player_select.height // 2
    pyautogui.click(x, y - 70)
    await asyncio.sleep(0.5)
    pyautogui.click(x, y - 70)

    await asyncio.sleep(2)
    invite_party = await wait_for_image(PATHS["invite_party"], confidence=0.7)
    

    x = invite_party.left + invite_party.width // 2
    y = invite_party.top + invite_party.height // 2

    pyautogui.moveTo(x,y)
    await asyncio.sleep(2.5)
    pyautogui.click(x, y)
    await asyncio.sleep(1)
    pyautogui.click(x, y)

    send_discord_log(webhookURL, f"Part invitation dispatched for bot instance {botId}." if botId else "Party invitation dispatched. Awaiting user response.")

    if botIP:
        url = f"{botIP}/bot_join"
        requests.post(url, json={"webhookURL": config.webhookURL})

    if not botId:
       await verifyInviteParty(webhookURL)

async def verifyInviteParty(webhookURL: str):
    await asyncio.sleep(2)
    timeout = 20

    while True:
        found = await wait_for_image(PATHS["joined_party"], confidence=0.7, timeout=1, dontRestart=True)
        if found:
            send_discord_log(webhookURL, "Invitation accepted by user. Proceeding with next operation.")
            press("esc")
            await asyncio.sleep(1)
            press("esc")

            # bots = config.json_config["followers"]

            # press("o")
         
            # for bot in bots:
            #     await asyncio.sleep(2)
            #     press("1")  
            #     type_string(bot["id"])
            #     search_button = await wait_for_image(PATHS["search_players"], confidence=0.7)
            #     pyautogui.click(search_button)
            #     await inviteToParty(webhookURL, bot["id"], bot["ip"])
            #     press('esc')
            
            # press('esc')
            press('esc')

            queue = await wait_for_image(PATHS["queue"], confidence=0.7, timeout=15)
            pyautogui.moveTo(queue)
            await asyncio.sleep(1)
            pyautogui.click(queue)
            send_discord_log(webhookURL, f"Queuing into {config.mode}. Searching.")
            await asyncio.gather(
            verifyPreLobby(webhookURL),
            verifyIfSearching(webhookURL)
            )
            break  

        timeout -= 1    
        if timeout <= 0:
            send_discord_log(webhookURL, "Player didn't join party on time. Restarting.")
            sendError(config.json_config["self_ip"])
            await reset()
            break

async def verifyFriend(activisionId: str, webhookURL: str):
    await asyncio.sleep(2)
    timeout = 120

    while True:
        press("1")  
        await asyncio.sleep(0.5)
        type_string(activisionId)

        search_button = await wait_for_image(PATHS["search_players"], confidence=0.7)
        if not search_button:
            break

        pyautogui.click(search_button)
        await asyncio.sleep(5)
        pyautogui.moveRel(0, 50)

        not_found = await wait_for_image(PATHS["not_found"], confidence=0.7, timeout=3, dontRestart=True)
        if not_found:
            press("1") 
            timeout -= 30
            if timeout <= 0:
                send_discord_log(webhookURL, "Invite was not accepted on time, session cancelled.")
                sendError(config.json_config["self_ip"])
                break
            await asyncio.sleep(30)
            continue

        send_discord_log(webhookURL, f"User {activisionId} verified in friend list. Sending party invitation.")
        await inviteToParty(webhookURL)
        break  



async def inviteFriend(activisionId: str, webhookURL: str):
    press("o")
    await asyncio.sleep(2)
    press("5")
    await asyncio.sleep(2)

    input_field = await wait_for_image(PATHS["input"], confidence=0.7)
    if not input_field: return

    pyautogui.click(input_field)
    time.sleep(0.5)
    pyautogui.click(input_field)
    time.sleep(1.5)

    type_string(activisionId)

    request_btn = await wait_for_image(PATHS["send_request"], confidence=0.7)
    if not request_btn: return

    pyautogui.moveTo(request_btn)
    await asyncio.sleep(1.25)
    pyautogui.click(request_btn)
    await asyncio.sleep(1.25)

    wait_timeout = 5
    while True:
        success =  await wait_for_image(PATHS["request_sent"], confidence=0.7, timeout=1,dontRestart=True)
        err = await wait_for_image(PATHS["failed_send"], confidence=0.7, timeout=1,dontRestart=True)
        if success:
            send_discord_log(webhookURL, f"Party Invitiation was sent successfully to player {activisionId}")
            press("o")
            await asyncio.sleep(2)
            press("o")
            await verifyFriend(activisionId, webhookURL)
            break

        if err:
            errorTxt = await detect_error_detail()
            if "already" in errorTxt:
                send_discord_log(webhookURL, f"User {activisionId} already present in friend list. Continuing.")
                press("o")
                await asyncio.sleep(2)
                press("o")
                await verifyFriend(activisionId, webhookURL)
                break
            await reset()
            send_discord_log(webhookURL, f"Party Invitiation failed for {activisionId} | **{errorTxt}**, cancelling session.")
            sendError(config.json_config["self_ip"])
            break

        wait_timeout -= 0.1
        if wait_timeout <= 0:
            send_discord_log(webhookURL,  f"Party Invitiation failed for {activisionId}, failure to recognize image. Raise this issue to staff!")
            break


async def selectMode(payload: StartRequest):
    battleroyale = await wait_for_image(PATHS["battleroyale"], confidence=0.85)
    resurgence = await wait_for_image(PATHS["resurgence"], confidence=0.85)

    if battleroyale and resurgence:
        btn = battleroyale if payload.mode == "BattleRoyale" else resurgence
        pyautogui.click(btn)
        await asyncio.sleep(1)
        pyautogui.click(btn)
        await asyncio.sleep(2.5)

        quads = await wait_for_image(PATHS["quads"], confidence=0.9)
        if quads:
            pyautogui.click(quads)
            await asyncio.sleep(1)
            pyautogui.click(quads)
            await asyncio.sleep(3)

        # await setPartyInviteOnly()
        await asyncio.sleep(2)
        await inviteFriend(payload.activision_id, payload.webhookURL)

async def run_game_flow(payload: StartRequest):
    await asyncio.sleep(5)
    global start_time
    start_time = time.monotonic()
    await selectWarzone()
    await selectMode(payload)

    for _ in range(12):
        exit_btn = await wait_for_image(PATHS["exit"], confidence=0.7, timeout=3, dontRestart=True)
        if exit_btn:
            pyautogui.click(exit_btn)
            await asyncio.sleep(0.5)
            pyautogui.click(exit_btn)

        battlepass = await wait_for_image(PATHS["continue_battlepass"], confidence=0.7, timeout=3, dontRestart=True)
        if battlepass:
            pyautogui.click(battlepass)
            await asyncio.sleep(0.5)
            pyautogui.click(battlepass)

        await asyncio.sleep(5)
