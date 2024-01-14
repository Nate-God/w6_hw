from app import app, db
from datetime import datetime
from flask import request
from app.models import Task




#due date has no time because I figure bigger tasks where time is less important (tasks example had the same time for all entries with different days) also style for yyyy-mm-ddThh:mm:ss kinda annoying^^ 

@app.route('/')
def index():
    first_name = 'Nathaniel'
    last_name = 'Godfrey'
    return f'Hello World!! - From {first_name} {last_name}, now go find tasks to do!'


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created": task.created.strftime('%Y-%m-%dT%H:%M:%S'),
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
        }
        for task in tasks
    ]
    return task_list

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return {"error": "Task not found"}, 404

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created": task.created.strftime('%Y-%m-%dT%H:%M:%S'),
        "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None
    }


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if 'title' not in data or 'description' not in data:
        return {"error": "Title and description are required fields"}, 400
    
    due_date_str = data.get('due_date')
    if due_date_str:
        if due_date_str[4] != "-" and due_date_str[7] != "-" and len(due_date_str) != 10:
            return {"error": "bad date format on request; should be 'yyyy-mm-dd'"}, 412
        else:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    else:
        due_date = None

    new_task = Task(
        title=data['title'],
        description=data['description'],
        completed=data.get('completed', False),
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed": new_task.completed,
        "created": new_task.created,
        "due_date": due_date
    }, 201