#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


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



sqlite_file_name = "todo_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/todo/", response_model=ToDoRead)
def create_todo(*, session: Session = Depends(get_session), todo: ToDoCreate):
    db_todo = ToDo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/todo/", response_model=List[ToDo])
def read_todos(*, session: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=100, lte=100),
               token: str = Depends(oauth2_scheme)):
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
def update_hero(*, session: Session = Depends(get_session), todo_id: int, todo: ToDoUpdate):
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