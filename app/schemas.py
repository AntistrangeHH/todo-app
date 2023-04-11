from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
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
