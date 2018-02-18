import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder import models

class TodoList(Resource):
    def get(self, listId):
        todoList = models.TodoList.query.filter_by(id=listId).first()
        try:
            return {'user': todoList.user.username, 'name': todoList.name}
            # return todoList.__dict__
        except:
            return {}, 404
