import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from todoReminder.models.helpers import errorOnNone

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(350), unique=True, nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'))
    todo_list = db.relationship('TodoList',
        backref=db.backref('todo_item', lazy=True))

    def __repr__(self):
        return '<TodoItem %r>' % self.text
