# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends , HTTPException, status, Query
from fastapi_todo_app.Models.models import Todo, TodoCreate,TodoResponse,TodoUpdate
from fastapi_todo_app.Models.models import User,UserCreate,UserResponse,UserUpdate
from fastapi_todo_app.Utils.utils import create_db_and_tables, engine, get_session



# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app : FastAPI = FastAPI(lifespan=lifespan, title="Todo App with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        },
        {
            "url": "http://localhost:3000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Environment Server"
        }
        ],
        
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Create a new todo list
@app.post("/todos/", response_model=TodoCreate)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


# Get All Todos
@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)], offset: int =Query(default=0,le=4), limit : int = Query(default=1,le=20)):
        todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
        return todos

# Get Single Todo

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
   single_todo =  session.get(Todo, todo_id)
   if not single_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
   return single_todo


#Delete the todos
@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted"}



# Update Todo
@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
    
    todo_dict = todo.model_dump(exclude_unset=True)

    for key, value in todo_dict.items():
         setattr(todo, key, value)
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo



# Get All Users
@app.get("/users/", response_model=list[User])
def read_users(session: Annotated[Session, Depends(get_session)], offset: int =Query(default=0,le=4), limit : int = Query(default=1,le=20)):
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        return users

# Get Single User
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

# Create User
@app.post("/users/", response_model=UserCreate)
def create_user(user: User, session: Annotated[Session, Depends(get_session)]):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Delete User
@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}

# Update User

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user_dict = user.model_dump(exclude_unset=True)

    for key, value in user_dict.items():
         setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

