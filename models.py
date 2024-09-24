from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    projects = db.relationship('Project', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) 
    description = db.Column(db.String(500), nullable=True)  
    due_date = db.Column(db.DateTime, nullable=True)  
    is_completed = db.Column(db.Boolean, default=False) 
    priority = db.Column(db.Integer, default=0)  
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)  
    subtasks = db.relationship('SubTask', backref='task', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    def __repr__(self):
        return f'<Task {self.name}>'

class SubTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) 
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)  
    due_date = db.Column(db.DateTime, nullable=True)  
    is_completed = db.Column(db.Boolean, default=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  