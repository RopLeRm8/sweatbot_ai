from typing import Literal
from pydantic import BaseModel

class StartRequest(BaseModel):
    activision_id: str
    mode: Literal["BattleRoyale", "Resurgence"]
    webhookURL: str

class LeavePayload(BaseModel):
    webhookURL: str | None = None