from fastapi import FastAPI

from app.core.logging import setup_logger
from app.ui import admin, login, user
from app.ui.middleware import LoggerMiddleware

logger = setup_logger()

app = FastAPI()

app.add_middleware(LoggerMiddleware)

app.include_router(user.router)
app.include_router(login.router)
app.include_router(admin.router)
