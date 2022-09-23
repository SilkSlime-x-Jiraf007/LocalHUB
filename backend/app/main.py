from urllib.request import Request
from fastapi import Depends, FastAPI, HTTPException, status, Header, Request
from app import routers
from app.auth import authRouter, User, get_user
from user_agents import parse

app = FastAPI()

app.include_router(authRouter, prefix="/auth", tags=["auth"])
