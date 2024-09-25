from flask import Blueprint, request, jsonify
from models import db, Task, SubTask, Project, User
from datetime import datetime, date

bp = Blueprint('main', __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        image = data.get('image')  

        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        new_user = User(username=username, email=email, password=password, image=image)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'id': new_user.id, 'username': new_user.username}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'taskName': task.name,
        'dueDate': task.due_date,
        'isCompleted': task.is_completed,
        'subTasks': [{
            'id': sub.id,
            'taskName': sub.name,
            'dueDate': sub.due_date,
            'isCompleted': sub.is_completed,
        } for sub in task.subtasks]
    } for task in tasks])

@bp.route('/api/tasks/today', methods=['GET'])
def get_today_tasks():
    try:
        today = date.today()
        #today = datetime.date.today()
        tasks = Task.query.filter(db.func.date(Task.due_date) == today).all()
        task_list = [{
            "id": t.id,
            "name": t.name, 
            "dueDate": t.due_date.isoformat(),
            "completed": t.is_completed 
        } for t in tasks]
        return jsonify(task_list), 200
    except Exception as e:
        print(f"Error retrieving today's tasks: {e}")
        return jsonify({"error": "Failed to load today's tasks"}), 500
    
@bp.route('/api/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    try:
        today = date.today()
        #today = datetime.date.today()
        tasks = Task.query.filter(db.func.date(Task.due_date) < today, Task.is_completed == False).all()
        task_list = [{
            "id": t.id,
            "name": t.name, 
            "dueDate": t.due_date.isoformat(),
            "completed": t.is_completed  
        } for t in tasks]
        return jsonify(task_list), 200
    except Exception as e:
        print(f"Error retrieving overdue tasks: {e}")
        return jsonify({"error": "Failed to load overdue tasks"}), 500

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({'error': 'project_id is required'}), 400

    project = Project.query.get(project_id)
    if project is None:
        return jsonify({'error': 'Invalid project_id: Project does not exist'}), 400

    new_task = Task(
        name=data.get('name'),
        description=data.get('description'),
        due_date=data.get('due_date'),
        is_completed=data.get('is_completed', False),
        priority=data.get('priority', 0),
        project_id=project_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201


@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.json
    task.name = data.get('taskName', task.name)
    task.due_date = data.get('dueDate', task.due_date)
    task.is_completed = data.get('isCompleted', task.is_completed)
    
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})


@bp.route('/subtasks', methods=['POST'])
def create_subtask():
    data = request.json
    id = data.get('parentId')
    existing_task = Task.query.get(id)
    
    if not existing_task:
        return jsonify({'error': 'Parent task not found'}), 404

    new_subtodo = SubTask(
        name=data.get('taskName'),
        due_date=data.get('dueDate'),
        is_completed=data.get('isCompleted', False),
        task_id=id
    )
    db.session.add(new_subtodo)
    db.session.commit()
    return jsonify({'message': 'SubTodo created successfully'}), 201


@bp.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        projects = Project.query.all()
        project_list = [{
            "_id": p.id,
            "name": p.name,
            "user_id": p.user_id,
            "tasks": [{"id": task.id, "name": task.name} for task in p.tasks]
        } for p in projects]
        return jsonify(project_list), 200
    except Exception as e:
        print(f"Error retrieving projects: {e}")
        return jsonify({"error": "Failed to load projects"}), 500

@bp.route('/api/tasks/completed', methods=['GET'])
def get_completed_todos():
    try:
        todos = Task.query.filter_by(is_completed=True).all()
        todo_list = [{
            "id": t.id,
            "name": t.name,
            "completed": t.is_completed
        } for t in todos]
        return jsonify(todo_list), 200
    except Exception as e:
        print(f"Error retrieving completed todos: {e}")
        return jsonify({"error": "Failed to load completed todos"}), 500

@bp.route('/api/tasks/incomplete', methods=['GET'])
def get_incomplete_task():
    try:
        todos = Task.query.filter_by(is_completed=False).all()
        todo_list = [{
            "id": t.id,
            "name": t.name,
            "completed": t.is_completed
        } for t in todos]
        return jsonify(todo_list), 200
    except Exception as e:
        print(f"Error retrieving incomplete todos: {e}")
        return jsonify({"error": "Failed to load incomplete todos"}), 500

@bp.route('/api/tasks/total', methods=['GET'])
def get_total_task():
    try:
        total_count = Task.query.count()
        return jsonify(total_count), 200
    except Exception as e:
        print(f"Error retrieving total todos count: {e}")
        return jsonify({"error": "Failed to load total todos count"}), 500

@bp.route('/projects', methods=['POST'])
def create_project():
    try:
        data = request.json
        name = data.get('name')
        user_id = data.get('user_id')  

        if not name:
            return jsonify({'error': 'Project name is required'}), 400

        if not user_id:  
            return jsonify({'error': 'User ID is required'}), 400

        new_project = Project(name=name, user_id=user_id)  
        db.session.add(new_project)
        db.session.commit()

        return jsonify({'id': new_project.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


import logging
from flask import abort

@bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting project: {str(e)}")  
        if "404" in str(e): 
            abort(404, description="Project not found.")
        return jsonify({'error': str(e)}), 500


    
@bp.route('/search', methods=['GET'])
def search_tasks():
    query = request.args.get('query', '').lower()
    print(f"Search query: {query}") 
    results = Task.query.filter(Task.name.ilike(f'%{query}%')).all()
    
    print(f"Results found: {len(results)}")  
    for task in results:
        print(f"Task: {task.name}") 
    
    tasks_list = [
        {"id": task.id, "name": task.name, "description": task.description, "isCompleted": task.is_completed}
        for task in results
    ]

    return jsonify(tasks_list)
