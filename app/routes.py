from app import app, db
from datetime import datetime
from flask import request
from app.models import Task, User
from app.auths import basic_auth, token_auth




#due date has no time because I figure bigger tasks where time is less important (tasks example had the same time for all entries with different days) also style for yyyy-mm-ddThh:mm:ss kinda annoying^^ 

@app.route('/')
def index():
    first_name = 'Nathaniel'
    last_name = 'Godfrey'
    return f'Hello World!! - From {first_name} {last_name}, now go find tasks to do!'

@app.route('/token')
@basic_auth.login_required
def get_token():
    current_user = basic_auth.current_user()
    return {'token':current_user.get_token(),'token_expiration': current_user.token_expiration} 

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
@token_auth.login_required
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

@app.route('/tasks', methods=['DELETE'])
@token_auth.login_required

def delete_task(task_id):
    task = db.session.get(Task,task_id)
    if task is None:
        return {"error": "Task not found"}, 404

    # Check if the current user is the owner of the task
    if task.user_id != token_auth.current_user().id:
        return {"error": "not authorized"}, 403


    db.session.delete(task)

    return {"message": "Task deleted successfully"}, 200

# {
#     "title":"hhff",
#     "description":"hfhfjf"
# }

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return {"error": "username, email and password are required fields"}, 400
    

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    new_user.set_password(data['password'])
    new_user.save()

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "password": new_user.password,
        "created": new_user.created
        }, 201


@app.route('/user/<int:user_id>', methods=['DELETE'])
@token_auth.login_required

def delete_user(user_id):

    user = db.session.get(User,user_id)
    current_user = token_auth.current_user()
    if user is None:
        return {"error": "Task not found"}, 404

    # Check if the current user is the owner of the task
    if user != current_user:
        return {"error": "not authorized"}, 403

    user.delete_user()
    return {"message": "user deleted successfully"}, 200
#{ 
# "username":"Ricardo_num_1",
#     "email":"hdhdhd",
#     "password":"abc123"
# }


@app.route('/users', methods=['DELETE'])
@token_auth.login_required

def delete_users():
    db.session.delete(token_auth.current_user())

    return {"message": "user deleted successfully"}, 200