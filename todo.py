#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ToDo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    details: str


class ToDoCreate(SQLModel):
    title: str
    details: str


class ToDoRead(SQLModel):
    id: int
    title: str
    details: str


sqlite_file_name = "todo_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/todo/", response_model=ToDoRead)
def create_todo(todo: ToDoCreate):
    with Session(engine) as session:
        db_todo = ToDo.from_orm(todo)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo


@app.get("/todo/", response_model=List[ToDo])
def read_todo():
    with Session(engine) as session:
        todo = session.exec(select(ToDo)).all()
        return todo


@app.delete("/heroes/{hero_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(ToDo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"ok": True}