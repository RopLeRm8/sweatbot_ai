from pydirectinput import press
import asyncio

async def reset():
    press("esc")
    await asyncio.sleep(1.5)
    press("esc")
    await asyncio.sleep(1.5)
    press("esc")
    await asyncio.sleep(1.5)
    press("esc")
