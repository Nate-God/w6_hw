from datetime import datetime, timedelta
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os
import re
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True, default=None)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_task(self):
        db.session.delete(self)
        db.session.commit()

    # def __init__(self,**kwarfs):
    #     allowed_fields = {'title', 'description'}

    # def update(self, **kwargs):


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index = True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.set_password(**kwargs.get("password", ''))
    #     pass

    # def update(self,**kwargs):
    #     allowed_fields = {"username", "password", "email"}

        # def camel_to_snake(string):
        #     return re.sub("([A-Z][A-Za-z]*)", "_\1", string).lower()
        # for key, value in kwargs.items():
        #     snake_key = camel_to_snake(key)
        #     if snake_key in allowed_fields:
        #         if snake_key == 'password':
        #             self.set_password(value)
        #         else:
        #             setattr(self, snake_key, value)
        # self.save()

    def set_password(self,password):
        self.password = generate_password_hash(password)
        self.get_token()
        self.save()

    def check_password(self, plain_text_password):
        return check_password_hash(self.password, plain_text_password)

    def get_token(self):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(hours=1)
        self.save()
        return self.token

    def to_dict(self):
        return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password,
        "created": self.created
        }

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()