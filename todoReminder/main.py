import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import todoReminder.views as views
from todoReminder import app
from todoReminder import db
from todoReminder.models import __initAdmin

# TODO: Show admin todoItems
# TODO: Delete todoItems
# TODO: Marshmallow schema
# TODO: Set time for todo item
# TODO: The UI should allow the user to quickly create a reminder due today
# or tomorrow
# TODO: Connect User to Google Account
# TODO: Create Google Calendar Event from Todo
# TODO: Flask Migrate

app, api = views.viewConstructor(app)
try:
    db.create_all()
    __initAdmin()
except:
    pass
if __name__ == '__main__':
    app.run()
