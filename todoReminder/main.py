import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import views
from todoReminder import app
from todoReminder import db
from todoReminder.models import __initAdmin

# TODO: Show admin todoItems
# TODO: Delete todoItems
# TODO: Set time for todo item
# TODO: The UI should allow the user to quickly create a reminder due today
# or tomorrow
# TODO: Connect User to Google Account
# TODO: Create Google Calendar Event from Todo
# TODO: Migrate schema without data loss?

app, api = views.viewConstructor(app)

if __name__ == '__main__':
    # db.create_all()
    try:
        __initAdmin()
    except:
        pass
    app.run()
