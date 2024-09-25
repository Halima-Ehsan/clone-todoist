# clone-todoist

## Installation
# Prerequisites
- Python 3.8+
- Flask
- Virtualenv (optional but recommended)

# Overview
This project is a simple backend API for a Todoist-clone, inspired by Todoist. It allows users to manage tasks by adding, editing, deleting, and organizing them into projects or lists. The API is built using Flask.

# Features
- Create, read, update, and delete tasks (CRUD).
- Organize tasks by projects.
- Set deadlines and priorities for tasks.
- Mark tasks as completed or uncompleted.

# Technologies Used
- Python
- Flask (Version:3.0.3)
- SQLAlchemy (Version: 2.0.35)

## API Endpoints
# Tasks
GET /api/tasks: Get all tasks.
POST /tasks: Create a new task.
GET /api/tasks/overdue: Get a overdue task.
GET api/tasks/today: Get a today task.
PUT /tasks/<task_id>: Update an existing task.
DELETE /tasks/<task_id>: Delete a task.
GET /api/tasks/completed: Get completed tasks.
GET /api/tasks/incomplete: Get incomplete tasks.
GET /search: Get searched task.

# Projects
GET /api/projects: Get all projects.
POST /projects: Create a new project.
DELETE /projects/<project_id>: Delete a project.
