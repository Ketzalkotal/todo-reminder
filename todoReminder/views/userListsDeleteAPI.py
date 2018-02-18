import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder.models import User
from todoReminder.models import TodoList
from todoReminder.models import TodoItem

class UserListsDeleteAPI(Resource):
    def delete(self, username, listID):
        # user = User.query.filter_by(username=username).first()
        # don't need username
        try:
            todoList = TodoList.query.filter_by(id=listID).first()
            db.session.delete(todoList)
            db.session.commit()
            return {"status": "success"}
        except:
            return {}, 404
