from flask import Flask, Blueprint, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import views

basedir = os.path.abspath(os.path.dirname(__file__))
# the to_json helper method may need to be able to detect circular references
# could pass a context that holds enough information to detect these circular references

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/todoReminder.db' % basedir
db = SQLAlchemy(app)
