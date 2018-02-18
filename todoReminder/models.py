import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import views
from todoReminder import db

def errorOnNone(fun):
    def helper(*args, **kwargs):
        returnVal = fun(*args, **kwargs)
        if returnVal == None:
            raise ValueError("Function {} returns None".format(fun))
        return returnVal
    return helper

# todoReminder.models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # the to_json helper method may need to be able to detect circular references
    # could pass a context that holds enough information to detect these circular references
    def to_json(self):
        return {
            'username': self.username,
            'email': self.email
        }

    @classmethod
    @errorOnNone
    def filter_json(cls, input_json):
        """Simplifies Querying DB with API supplied JSON
        """
        if input_json.get('id'):
            return cls.query.filter_by(id=input_json.get('id')).first()
        if input_json.get('email'):
            return cls.query.filter_by(email=input_json.get('email')).first()
        if input_json.get('username'):
            return cls.query.filter_by(username=input_json.get('username')).first()

    def __repr__(self):
        return '<User %r>' % self.username

class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('todo_list', lazy=True))

    def to_json(self, related=[]):
        # default values
        result = {
            'name': self.name,
            'id': self.id
        }
        if 'user' in related:
            result['user'] = self.user.to_json()
        return result

    def from_json(self, input_json):
        print 'in from_json'
        print input_json
        self.name = input_json.get('name', self.name)
        user_json = input_json.get('user') # nested object / dict
        if user_json:
            try:
                self.user = User.filter_json(user_json) # just contains user fields
                print self.user
            except:
                raise ValueError("TodoList.from_json: User Missing")

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(350), unique=True, nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'))
    todo_list = db.relationship('TodoList',
        backref=db.backref('todo_item', lazy=True))

    def __repr__(self):
        return '<TodoItem %r>' % self.text

def __initAdmin():
    admin = User(username="admin", email="admin@gmail.com")
    db.session.add(admin)
    db.session.commit()
    print [user.id for user in User.query.all()]
    print User.query.filter_by(id=1).first()

def __initList():
    admin = User.query.filter_by(id=1).first()
    todoList = TodoList(name='Test List', user=admin)
    db.session.add(todoList)
    db.session.commit()
