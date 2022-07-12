#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


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
def read_todos(offset: int = 0, limit: int = Query(default=100, lte=100)):
    """
    Read todos.
    Returns the first results from database (offset=0), and a maximum of 100 todos (limit 100)
    """
    with Session(engine) as session:
        todos = session.exec(select(ToDo).offset(offset).limit(limit)).all()
        return todos


@app.get("/todo/{todo_id}", response_model=ToDoRead)
def read_todo(todo_id: int):
    """Read hero based on hero_id"""
    with Session(engine) as session:
        todo = session.get(ToDo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo


@app.patch("/heroes/{hero_id}", response_model=ToDoRead)
def update_hero(todo_id: int, todo: ToDoUpdate):
    with Session(engine) as session:
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


@app.delete("/heroes/{hero_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(ToDo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"ok": True}