import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from user import User

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
