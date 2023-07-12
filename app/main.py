from fastapi import FastAPI

from app.api import admin, login, user

app = FastAPI()

app.include_router(user.router)
app.include_router(login.router)
app.include_router(admin.router)
