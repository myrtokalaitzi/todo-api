from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Simple To-Do List API",
    description="A basic in-memory CRUD API for managing tasks",
    version="1.0.0"
)

# In-memory storage
tasks = {}
counter = 1

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    done: bool = False
    created_at: str

@app.get("/")
def root():
    return {"message": "To-Do List API is running!", "total_tasks": len(tasks)}

@app.get("/tasks")
def get_all_tasks():
    return {"tasks": list(tasks.values()), "count": len(tasks)}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global counter
    new_task = {
        "id": counter,
        "title": task.title,
        "description": task.description,
        "done": False,
        "created_at": datetime.utcnow().isoformat()
    }
    tasks[counter] = new_task
    counter += 1
    return new_task

@app.patch("/tasks/{task_id}/done")
def mark_done(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id]["done"] = True
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted = tasks.pop(task_id)
    return {"message": f"Task '{deleted['title']}' deleted successfully"}
