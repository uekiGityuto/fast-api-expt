import os
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.hash import verify_password

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Error Messages
ERROR_LOGIN_FAILURE = "LOGIN_FAILURE"
ERROR_INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
ERROR_INACTIVE_USER = "INACTIVE_USER"
ERROR_UNAUTHORIZED_OPERATION = "UNAUTHORIZED_OPERATION"
ERROR_USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
ERROR_USER_NOT_FOUND = "USER_NOT_FOUND"


def _raise_http_exception(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        _raise_http_exception(status.HTTP_403_FORBIDDEN, ERROR_LOGIN_FAILURE)
    assert user is not None
    if not verify_password(password, user.hashed_password):
        _raise_http_exception(status.HTTP_403_FORBIDDEN, ERROR_LOGIN_FAILURE)
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ERROR_INVALID_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # type: ignore
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: schemas.User = Depends(get_current_user)) -> schemas.User:
    if not current_user.active:
        _raise_http_exception(status.HTTP_400_BAD_REQUEST, ERROR_INACTIVE_USER)
    return current_user


def get_current_admin_user(current_user: schemas.User = Depends(get_current_active_user)) -> schemas.User:
    if not current_user.admin:
        _raise_http_exception(status.HTTP_403_FORBIDDEN,
                              ERROR_UNAUTHORIZED_OPERATION)
    return current_user


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        _raise_http_exception(status.HTTP_400_BAD_REQUEST,
                              ERROR_USER_ALREADY_EXISTS)
    return crud.create_user(db=db, user=user)


@app.get("/admin/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: models.User = Depends(get_current_admin_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/admin/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), _: models.User = Depends(get_current_admin_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        _raise_http_exception(status.HTTP_404_NOT_FOUND, ERROR_USER_NOT_FOUND)
    return db_user


@app.post("/admin/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_admin_user)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/admin/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: models.User = Depends(get_current_admin_user)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
