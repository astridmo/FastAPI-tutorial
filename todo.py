#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext


SECRET_KEY = "3051c8f0f2e233b56703892b7dfbbe1f7f4ff1befb7964aa05e6800c6eb3898b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =================================
# Classes for autheitication
# =================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(SQLModel):
    #id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(primary_key=True)
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(UserBase, table=True):
    hashed_password: str

# =============================
# Classes for ToDo
# =============================
class ToDoBase(SQLModel):
    title: str = Field(index=True)
    details: str


class ToDo(ToDoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ToDoCreate(ToDoBase):
    """Create a ToDo"""
    pass


class ToDoRead(ToDoBase):
    """Read ToDo's"""
    id: int


class ToDoUpdate(SQLModel):
    title: Optional[str] = None
    details: Optional[str] = None


# =======================================
#
# =======================================

sqlite_file_name = "todo_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ================================
# Functions for authentication
# ================================


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    with Session(engine) as session:
        user = session.get(UserInDB, username)
        return user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: UserBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/user/{user_id}", response_model=UserBase)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    """Read hero based on hero_id"""
    todo = session.get(UserInDB, user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# =================================
# Functions for todo
# =================================






@app.post("/todo/", response_model=ToDoRead)
def create_todo(*, session: Session = Depends(get_session), todo: ToDoCreate):
    db_todo = ToDo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/todo/", response_model=List[ToDo])
def read_todos(*, session: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=100, lte=100),
               current_user: UserBase = Depends(get_current_user)):
    """
    Read todos.
    Returns the first results from database (offset=0), and a maximum of 100 todos (limit 100)
    """
    todos = session.exec(select(ToDo).offset(offset).limit(limit)).all()
    return todos


@app.get("/todo/{todo_id}", response_model=ToDoRead)
def read_todo(*, session: Session = Depends(get_session), todo_id: int):
    """Read hero based on hero_id"""
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/todo/{todo_id}", response_model=ToDoRead)
def update_todo(*, session: Session = Depends(get_session), todo_id: int, todo: ToDoUpdate):
    db_todo = session.get(ToDo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete("/todo/{todo_id}")
def delete_todo(*, session: Session = Depends(get_session), todo_id: int):
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}
