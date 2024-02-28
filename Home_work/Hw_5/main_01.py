# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.


from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool


tasks_db = []


@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    tasks_db.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    task_in_db = next((t for t in tasks_db if t.id == task_id), None)
    if task_in_db is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_in_db.title = task.title
    task_in_db.description = task.description
    task_in_db.status = task.status
    return task_in_db


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db.remove(task)
    return task

# пример curl запроса
# curl -X POST "http://127.0.0.1:8000/tasks/" -H "Content-Type: application/json" -d '{"id": 1, "title": "Новая задача", "description": "Описание новой задачи", "status": false}'