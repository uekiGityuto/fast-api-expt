from fastapi import FastAPI

from app.api import admin, login, users

app = FastAPI()

app.include_router(users.router)
app.include_router(login.router)
app.include_router(admin.router)
