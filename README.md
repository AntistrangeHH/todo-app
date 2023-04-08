# To-Do List API

A simple To-Do List API built using FastAPI, SQLAlchemy, and SQLite.

## Features

- Add a to-do
- Change a to-do
- Delete a to-do (soft delete)
- List all todos
- Return a todo
- Login
- Return a user

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn

## Getting Started

1. Clone the repository

```bash
git clone https://github.com/yourusername/todo_app.git
cd todo_app
```

2. Create a virtual environment and activate it
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
uvicorn app.main:app --reload
```

The To-Do List API will be accessible at http://localhost:8000.

## Docker

1. Build the Docker image

```bash
docker build -t todo_app .
```

2. Run the Docker container

```bash
docker run -d -p 8000:8000 todo_app
```

The To-Do List API will be accessible at http://localhost:8000.

## API Endpoints

- `POST /users`: Create a new user
- `GET /users/{user_id}`: Retrieve a user by ID
- `POST /todos`: Create a new to-do
- `GET /todos/{todo_id}`: Retrieve a to-do by ID
- `GET /todos`: List all todos
- `PUT /todos/{todo_id}`: Update a to-do
- `DELETE /todos/{todo_id}`: Soft delete a to-do

## Database Migrations with Alembic

Alembic is a lightweight database migration tool for SQLAlchemy. It helps manage and track changes to your database schema.

### Configuration
1. To use Alembic, ensure you have the required packages installed:

```bash
pip install -r requirements.txt
```
2. Initialize Alembic in your project:

```bash
alembic init alembic
```

3. Update the `alembic.ini` file to point to your database URL
4. Modify the `env.py` file inside the `alembic` folder to include the following:
```python
from app.models import Base
target_metadata = Base.metadata
```
### Usage
1. To create a new migration, run:

```bash
alembic revision -m "Your migration message"
```
2. Edit the generated migration file and add the necessary upgrade() and downgrade() operations
3. Apply the migration to your database by running:

```bash
alembic upgrade head
```
4. If you need to undo the latest migration, run:

```bash
alembic downgrade -1
```
5. To view the migration history, run:

```bash
alembic history
```
6. To check the current migration version, run:

```bash
alembic current
```

For more information about Alembic and its features, visit the official documentation.
This version includes a section on how to configure and use Alembic for database migrations.


