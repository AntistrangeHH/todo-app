from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class ToDoCreate(BaseModel):
    title: str
    completed: bool

    class Config:
        orm_mode = True


class ToDoUpdate(BaseModel):
    title: str
    completed: bool

    class Config:
        orm_mode = True


class ToDo(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    class Config:
        orm_mode = True
