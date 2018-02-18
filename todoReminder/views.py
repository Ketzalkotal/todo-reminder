import os
from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from todoReminder import db
from models import User
from models import TodoList
from models import TodoItem

# api
class UserAPI(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {'email': user.email, 'username': user.username, 'id': id}

    def put(self, id):
        user = User.query.filter_by(id=id).first()
        data = request.form
        if not user:
            user = User(**data) # old from json
            print user
            db.session.add(user)
        else:
            for key, value in data.items():
                print key, value
                setattr(user, key, value)
        db.session.commit()
        print user
        return {'email': user.email, 'username': user.username, 'id': id}

class TodoListsAPI(Resource):
    def get(self):
        admin = User.query.filter_by(id=1).first()
        todoLists = TodoList.query.filter_by(user=admin).all()
        if todoLists:
            return [todoList.to_json() for todoList in todoLists]
        else:
            return {}, 404

    def put(self):
        todoList = TodoList()
        todoList.from_json(request.get_json()) # new from json because of user relation
        # try:
        #     todoList.from_json(request.get_json()) # new from json because of user relation
        # except ValueError:
        #     return {"message": "User Not Found"}, 404
        db.session.add(todoList)
        db.session.commit()
        try:
            return todoList.to_json()
        except AttributeError:
            return {"message": "User Not Found"}, 404

class UserListsAPI(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        # return TodoList.helper.filter_or_404(user=user)
        # TODO: replace below section with above line
        todoLists = TodoList.query.filter_by(user=user).all()
        if todoLists:
            return [todoList.to_json() for todoList in todoLists]
        else:
            return {}, 404

class UserListsDeleteAPI(Resource):
    def delete(self, username, listID):
        # user = User.query.filter_by(username=username).first()
        # don't need username
        try:
            todoList = TodoList.query.filter_by(id=listID).first()
            db.session.delete(todoList)
            db.session.commit()
            return {"status": "success"}
        except:
            return {}, 404

class TodoListAPI(Resource):
    def get(self, listId):
        todoList = TodoList.query.filter_by(id=listId).first()
        try:
            return {'user': todoList.user.username, 'name': todoList.name}
            # return todoList.__dict__
        except:
            return {}, 404

# urls
# /user/<username>/list/<id>
# /user/<username>/list
# returns all lists for user
# /user/<username>/list/<listId>
# /user/<username>/list/<listId>/<itemId>

def viewConstructor(app):
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(UserAPI, '/user/<int:id>')
    api.add_resource(UserListsAPI, '/user/<string:username>/todoLists')
    api.add_resource(UserListsDeleteAPI, '/user/<string:username>/todoList/<int:listID>')
    # below should only work with user verification
    api.add_resource(TodoListsAPI, '/todoList')
    api.add_resource(TodoListAPI, '/todoList/<int:listId>')
    app.register_blueprint(api_bp, url_prefix='/api')
    # SPA entrypoint
    @app.route('/')
    def index():
        return render_template('index.html')
    return app, api
