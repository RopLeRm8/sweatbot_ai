from fastapi import APIRouter, Header, HTTPException
from utils.state import get_ready
from logic.startup import launch_cod
from utils.schemas import StartRequest, LeavePayload
import logic.config as config
from logic.fillerbots_logic import join_party
from logic.game_flow import leaveGame
router = APIRouter()

@router.get("/status")

def status():
    return {"ready":get_ready()}

@router.post("/start")
async def start_game(
    payload:StartRequest,
    authorization: str = Header(None)
):
    if authorization != "Bearer oivavoi":
        raise HTTPException(status_code=403,detail="Unauthorized")
    
    if not get_ready():
        raise HTTPException(status_code=400,detail="Bot not ready")
    
    config.webhookURL = payload.webhookURL
    config.mode = payload.mode
    
    await launch_cod(payload)
    return {"status": "started"}

@router.post("/bot_join")
async def bot_join(payload: LeavePayload):
    config.webhookURL = payload.webhookURL
    await join_party()
    return "ok"

@router.post("/bot_leave")
async def bot_leave(payload: LeavePayload):
    config.webhookURL = payload.webhookURL
    await leaveGame(isLeader=False)
    return "ok"

