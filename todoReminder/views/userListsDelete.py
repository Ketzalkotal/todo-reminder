import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder import models

class UserListsDelete(Resource):
    def delete(self, username, listID):
        try:
            todoList = models.TodoList.query.filter_by(id=listID).first()
            db.session.delete(todoList)
            db.session.commit()
            return {"status": "success"}
        except:
            return {}, 404
