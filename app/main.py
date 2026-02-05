from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from db import Database

app = FastAPI(title="Task API", version="1.0.0")
db = Database()


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    await db.connect()
    await db.create_tables()


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown"""
    await db.disconnect()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"status": "healthy", "service": "Task API"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Task API"}


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    tasks = await db.get_all_tasks()
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = await db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    """Create a new task"""
    task_id = await db.create_task(task.title, task.description, task.completed)
    task.id = task_id
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    """Update an existing task"""
    updated = await db.update_task(task_id, task.title, task.description, task.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    task.id = task_id
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    deleted = await db.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
