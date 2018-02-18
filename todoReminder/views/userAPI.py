import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder.models import User
from todoReminder.models import TodoList
from todoReminder.models import TodoItem

# api
class UserAPI(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {'email': user.email, 'username': user.username, 'id': id}

    def put(self, id):
        user = User.query.filter_by(id=id).first()
        data = request.form
        if not user:
            user = User(**data) # old from json
            print user
            db.session.add(user)
        else:
            for key, value in data.items():
                print key, value
                setattr(user, key, value)
        db.session.commit()
        print user
        return {'email': user.email, 'username': user.username, 'id': id}
