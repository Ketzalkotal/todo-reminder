import os
from flask import Flask, Blueprint, request, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/todoReminder.db' % basedir
db = SQLAlchemy(app)
