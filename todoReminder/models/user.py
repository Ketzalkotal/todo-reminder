import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder.models.helpers import errorOnNone

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
