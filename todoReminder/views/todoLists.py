import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder import models

class TodoLists(Resource):
    def get(self):
        admin = models.User.query.filter_by(id=1).first()
        todoLists = models.TodoList.query.filter_by(user=admin).all()
        if todoLists:
            return [todoList.to_json() for todoList in todoLists]
        else:
            return {}, 404

    def put(self):
        todoList = models.TodoList()
        todoList.from_json(request.get_json()) # new from json because of user relation
        # try:
        #     todoList.from_json(request.get_json()) # new from json because of user relation
        # except ValueError:
        #     return {"message": "User Not Found"}, 404
        db.session.add(todoList)
        db.session.commit()
        try:
            return todoList.to_json()
        except AttributeError:
            return {"message": "User Not Found"}, 404