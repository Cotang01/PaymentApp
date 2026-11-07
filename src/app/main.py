from fastapi import FastAPI

from src.features.user.router import router as user_router

app = FastAPI()
app.include_router(user_router)


@app.get("/")
async def index():
    return {"message": "Hello World"}
