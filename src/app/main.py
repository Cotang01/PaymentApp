from fastapi import FastAPI

from src.app.handlers import register_exception_handlers
from src.features.accounts.router_auth import router as auth_router
from src.features.accounts.router_user import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
register_exception_handlers(app)


@app.get("/")
async def index():
    return {"message": "Hello World"}
