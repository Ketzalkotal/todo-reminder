from flask import Blueprint, render_template
from flask_restful import Api
from user import User
from userLists import UserLists
from userListsDelete import UserListsDelete
from todoLists import TodoLists
from todoList import TodoList

# urls
# /user/<username>/list/<id>
# /user/<username>/list
# returns all lists for user
# /user/<username>/list/<listId>
# /user/<username>/list/<listId>/<itemId>

def viewConstructor(app):
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(User, '/user/<int:id>')
    api.add_resource(UserLists, '/user/<string:username>/todoLists')
    api.add_resource(UserListsDelete, '/user/<string:username>/todoList/<int:listID>')
    # below should only work with user verification
    api.add_resource(TodoLists, '/todoList')
    api.add_resource(TodoList, '/todoList/<int:listId>')
    app.register_blueprint(api_bp, url_prefix='/api')
    # SPA entrypoint
    @app.route('/')
    def index():
        return render_template('index.html')
    return app, api
