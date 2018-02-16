from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os
import views
from todoReminder import app
from __init__ import db

# TODO: Delete todoLists
# TODO: Show admin todoItems
# TODO: Delete todoItems
# TODO: Set time for todo item
# TODO: The UI should allow the user to quickly create a reminder due today
# or tomorrow
# TODO: Connect User to Google Account
# TODO: Create Google Calendar Event from Todo
# TODO: Migrate schema without data loss?

app, api = views.viewConstructor(app)
# This decorator make sure that the API fails loudly

if __name__ == '__main__':
    db.create_all()
    app.run()
