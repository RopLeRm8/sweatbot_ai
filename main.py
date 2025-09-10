import asyncio
import uvicorn
from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI()
app.include_router(api_router)

async def main():

    config = uvicorn.Config(app, host="0.0.0.0", port=6969, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
