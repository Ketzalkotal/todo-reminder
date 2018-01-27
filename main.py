from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/todoReminder.db' % basedir
db = SQLAlchemy(app)

# SPA entrypoint
@app.route('/')
def index():
    return render_template('index.html')

# models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(350), unique=True, nullable=False)

    def __repr__(self):
        return '<TodoItem %r>' % self.text

# api
class UserAPI(Resource):
    def get(self, userId):
        if listId not in todoLists:
            return {}, 404
        return {'data': todoLists[listId]}

class TodoList(Resource):
    def get(self, listId):
        if listId not in todoLists:
            return {}, 404
        return {'data': todoLists[listId]}

class TodoItem(Resource):
    def get(self, listId, itemId):
        if  listId not in todoLists or \
            itemId not in todoLists.get(listId, {}):
                return {}, 404
        return {'data': todoLists[listId][itemId]}

# urls
api.add_resource(TodoList, '/<string:listId>')
api.add_resource(TodoItem, '/<string:listId>/<string:itemId>')
app.register_blueprint(api_bp, url_prefix='/api')

# manager
# db.create_all()

if __name__ == '__main__':
    app.run()
