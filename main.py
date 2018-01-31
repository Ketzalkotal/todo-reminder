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
    name = db.Column(db.String(350), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('todo_list', lazy=True))

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(350), unique=True, nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'))
    todo_list = db.relationship('TodoList',
        backref=db.backref('todo_item', lazy=True))

    def __repr__(self):
        return '<TodoItem %r>' % self.text

# api
class UserAPI(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        return {'email': user.email, 'username': user.username}

    def put(self, userId):
        name = request.form['data']
        new_user = User(name=name)
        db.add(new_user)
        db.commit()

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
api.add_resource(UserAPI, '/user/<string:username>')
api.add_resource(TodoList, '/todoList/<string:listId>')
api.add_resource(TodoItem, '/todoItem/<string:listId>/<string:itemId>')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    db.create_all()
    # admin = User(username='admin', email='admin@example.com')
    # db.session.add(admin)
    # db.session.commit()
    app.run()
