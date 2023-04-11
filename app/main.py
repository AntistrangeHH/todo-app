from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import authentication

from fastapi.security import OAuth2PasswordRequestForm

from . import models, schemas, crud

app = FastAPI()

models.Base.metadata.create_all(bind=models.engine)


# Dependency to get the session object
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoints
@app.get("/")
def get_homepage():
    return "Go to /docs to test the API"


@app.post("/login", response_model=schemas.Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", response_model=schemas.Token)
def signup(
        user_data: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    user = crud.create_user(db, user_data)
    if not user:
        raise HTTPException(status_code=400, detail="Failed to create user")
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(authentication.get_current_user)
):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/todos", response_model=schemas.ToDo)
def create_todo(
        todo: schemas.ToDoCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(authentication.get_current_user)
):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)


@app.get("/todos/{todo_id}", response_model=schemas.ToDo)
def get_todo(
        todo_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(authentication.get_current_user)
):
    todo = crud.get_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.get("/todos", response_model=List[schemas.ToDoCreate])
def get_todos(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(authentication.get_current_user)
):
    todos = crud.get_todos(db=db, skip=skip, limit=limit)
    return todos


@app.put("/todos/{todo_id}", response_model=schemas.ToDoCreate)
def update_todo(
        todo_id: int,
        todo: schemas.ToDoUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(authentication.get_current_user)

):
    updated_todo = crud.update_todo(db=db, todo=todo, todo_id=todo_id)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@app.delete("/todos/{todo_id}")
def soft_delete_todo(
        todo_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(authentication.get_current_user)
):
    deleted_todo = crud.soft_delete_todo(db=db, todo_id=todo_id)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted"}
