import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder import models

class User(Resource):
    def get(self, id):
        user = models.User.query.filter_by(id=id).first()
        return {'email': user.email, 'username': user.username, 'id': id}

    def put(self, id):
        user = models.User.query.filter_by(id=id).first()
        data = request.form
        if not user:
            user = models.User(**data) # old from json
            print user
            db.session.add(user)
        else:
            for key, value in data.items():
                print key, value
                setattr(user, key, value)
        db.session.commit()
        print user
        print 'put user'
        return {'email': user.email, 'username': user.username, 'id': id}
