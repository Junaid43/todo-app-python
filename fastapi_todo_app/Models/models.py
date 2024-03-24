from sqlmodel import Field, SQLModel,Relationship
from typing import Optional
from typing import List


class TodoBase(SQLModel):
    content: str
    is_done: Optional[bool] = False

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user:Optional["User"] = Relationship(back_populates="todos")


class TodoCreate(SQLModel):
    pass

class TodoResponse(TodoBase):
    id: int

class TodoUpdate(SQLModel):
    content: Optional[str] = None
    is_done: Optional[bool] = None


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None

class UserBase(SQLModel):
    username: str
    password: str
    email: str

class User(UserBase, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True)
    todos: List["Todo"] = Relationship(back_populates="user")
    hashed_password: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    todos: List[TodoResponse]

class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None



