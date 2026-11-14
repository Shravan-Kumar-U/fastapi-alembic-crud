from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Task
import os
from dotenv import load_dotenv

load_dotenv() # Loads the variables from .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()

# 2. The Database Dependency
def get_db():
    with Session(engine) as session:
        yield session

# 3. Create a Task Endpoint (POST)
@app.post("/tasks/")
def create_task(title: str, description: str = None, db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    
    # Refresh updates the Python object with data from the database (like the auto-generated ID)
    db.refresh(new_task) 
    return new_task

# 4. Get All Tasks Endpoint (GET)
@app.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks