from flask import Blueprint, render_template
from flask_restful import Api
from userAPI import UserAPI
from userListsAPI import UserListsAPI
from userListsDeleteAPI import UserListsDeleteAPI
from todoListsAPI import TodoListsAPI
from todoListAPI import TodoListAPI
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
