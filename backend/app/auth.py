import uuid
from fastapi import APIRouter, Form, Depends, HTTPException, status, Request
from pydantic import BaseModel, SecretStr
from passlib.context import CryptContext
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import timedelta, datetime
import os
from app import models
from app.utils import response
from user_agents import parse

# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 43200

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


authRouter = APIRouter()


# #############################################################################################


class User(BaseModel):
    sid: str
    username: str
    role: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class AuthSession(BaseModel):
    sid: str
    last_updated: datetime
    user_agent: str

# #############################################################################################

def get_user_agent(request: Request) -> str:
    return str(parse(request.headers.get("User-Agent")))

def token_create(sub: str, sid: str, expires_delta: timedelta, type: str) -> str:
    to_encode = {
        "sub": sub,
        "sid": sid,
        "type": type,
        "exp": datetime.utcnow() + expires_delta
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def tokens_create(username: str, sid: str) -> Tokens:
    return Tokens(
        access_token=token_create(username, sid, timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access"),
        refresh_token=token_create(username, sid, timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES), "refresh"),
    )


def user_get_by_username(db: Session, username: str) -> User | None:
    return db.query(models.User).filter(models.User.username.ilike(username)).first()



def get_user(db: Session = Depends(get_db), access_token: str = Depends(oauth2_scheme)) -> models.User:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        sid: str = payload.get("sid")
        type: str = payload.get("type")
        if type != "access":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Необходимо использовать access токен", {
                                "WWW-Authenticate": "Bearer"})
    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Истек срок действия access токена", {
                            "WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный access токен", {
                            "WWW-Authenticate": "Bearer"})
    db_user = db.query(models.User).filter(models.User.username == username).first()
    return User(sid=sid, username=db_user.username, role=db_user.role)

def get_admin_user(user: User = Depends(get_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Недостаточно прав", {
                            "WWW-Authenticate": "Bearer"})
    return user


def get_refresh(db: Session = Depends(get_db), refresh_token: str = Depends(oauth2_scheme), request: Request = None) -> Tokens:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        sid: str = payload.get("sid")
        type: str = payload.get("type")
        if type != "refresh":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Необходимо использовать refresh токен", {
                                "WWW-Authenticate": "Bearer"})
    except ExpiredSignatureError:
        db.query(models.Session).filter(models.Session.sid == sid).delete()
        db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Истек срок действия refresh токена. Сессия завершена.", {
                            "WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный refresh токен", {
                            "WWW-Authenticate": "Bearer"})

    session = db.query(models.Session).filter(
        models.Session.sid == sid).first()
    if session is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Сессии с таким refresh токеном не существует", {
                            "WWW-Authenticate": "Bearer"})
    if refresh_token != session.refresh_tokens[0]:
        db.query(models.Session).filter(
            models.Session.sid == session.sid).delete()
        db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Данный refresh токен уже был использован ранее. Сессия завершена в целях безопасности.", {
                            "WWW-Authenticate": "Bearer"})

    tokens = tokens_create(username, sid)
    if request:
        session.user_agent = get_user_agent(request)
    session.last_updated = datetime.now()
    session.refresh_tokens = [tokens.refresh_token, *session.refresh_tokens]
    db.commit()
    return tokens

# #############################################################################################


@authRouter.post("/signup", response_model=None)
def sign_up(username: str = Form(), password: SecretStr = Form(), db: Session = Depends(get_db), user: User = Depends(get_admin_user)):
    if user_get_by_username(db, username) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"Имя пользователя '{username}' уже занято")
    db.add(models.User(username=username,
           password_hash=pwd_context.hash(password.get_secret_value())))
    db.commit()
    return response(None, f"Пользователь {username} зарегистрирован!")


@authRouter.post("/signin", response_model=Tokens)
def sign_in(request: Request, username: str = Form(), password: SecretStr = Form(), db: Session = Depends(get_db)):
    user = user_get_by_username(db, username)
    if user is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Неверное имя пользователя")
    if not pwd_context.verify(password.get_secret_value(), user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Неверное пароль")

    sid = str(uuid.uuid4())
    tokens = tokens_create(user.username, sid)
    db.add(models.Session(
        sid=sid,
        username=user.username,
        last_updated=datetime.now(),
        user_agent=get_user_agent(request),
        refresh_tokens=[tokens.refresh_token]
    ))
    db.commit()
    return tokens


@authRouter.delete("/signout", response_model=None)
def sign_out(user: User = Depends(get_user), db: Session = Depends(get_db)):
    db.query(models.Session).filter(models.Session.username ==
                                     user.username).filter(models.Session.sid == user.sid).delete()
    db.commit()
    return response(None, "Сессия завершена")


@authRouter.post("/refresh/manual", response_model=Tokens)
def refresh_manual(refresh_token: str = Form(), db: Session = Depends(get_db)):
    return get_refresh(db, refresh_token)


@authRouter.post("/refresh", response_model=Tokens)
def refresh(tokens: Tokens = Depends(get_refresh)):
    return tokens


@authRouter.get("/sessions", response_model=None)
def get_all_sessions(user: str = Depends(get_user), db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(models.Session.username ==
                                                user.username).order_by(models.Session.last_updated.desc()).all()
    return response([AuthSession(**session.__dict__) for session in sessions])


@authRouter.delete("/sessions", response_model=None)
def terminate_all_sessions(user: User = Depends(get_user), db: Session = Depends(get_db)):
    db.query(models.Session).filter(models.Session.username ==
                                     user.username).filter(models.Session.sid != user.sid).delete()
    db.commit()
    return response(None, "Все остальные сессии завершены")


@authRouter.delete("/sessions/{sid}", response_model=None)
def terminate_session(sid: uuid.UUID, user: str = Depends(get_user), db: Session = Depends(get_db)):
    if str(sid) == user.sid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Выбранная сессия является текущей")
    db.query(models.Session).filter(models.Session.username ==
                                     user.username).filter(models.Session.sid == str(sid)).delete()
    db.commit()
    return response(None, "Выбранная сессия завершена")
