import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder.models import User
from todoReminder.models import TodoList
from todoReminder.models import TodoItem

class TodoListAPI(Resource):
    def get(self, listId):
        todoList = TodoList.query.filter_by(id=listId).first()
        try:
            return {'user': todoList.user.username, 'name': todoList.name}
            # return todoList.__dict__
        except:
            return {}, 404
