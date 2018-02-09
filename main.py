from flask import Flask, Blueprint, request, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os

# TODO: Delete todoLists
# TODO: Show admin todoItems
# TODO: Delete todoItems
# TODO: Set time for todo item
# TODO: The UI should allow the user to quickly create a reminder due today
# or tomorrow
# TODO: Connect User to Google Account
# TODO: Create Google Calendar Event from Todo
# TODO: Migrate schema without data loss?

basedir = os.path.abspath(os.path.dirname(__file__))
# the to_json helper method may need to be able to detect circular references
# could pass a context that holds enough information to detect these circular references

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/todoReminder.db' % basedir
db = SQLAlchemy(app)

# SPA entrypoint
@app.route('/')
def index():
    return render_template('index.html')

# This decorator make sure that the API fails loudly
def errorOnNone(fun):
    def helper(*args, **kwargs):
        returnVal = fun(*args, **kwargs)
        if returnVal == None:
            raise ValueError("Function {} returns None".format(fun))
        return returnVal
    return helper

# models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email
        }

    @classmethod
    @errorOnNone
    def filter_json(cls, input_json):
        """Simplifies Querying DB with API supplied JSON
        """
        if input_json.get('id'):
            return cls.query.filter_by(id=input_json.get('id')).first()
        if input_json.get('email'):
            return cls.query.filter_by(email=input_json.get('email')).first()
        if input_json.get('username'):
            return cls.query.filter_by(username=input_json.get('username')).first()

    def __repr__(self):
        return '<User %r>' % self.username

class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('todo_list', lazy=True))

    def to_json(self, related=[]):
        # default values
        result = {
            'name': self.name,
            'id': self.id
        }
        if 'user' in related:
            result['user'] = self.user.to_json()
        return result

    def from_json(self, input_json):
        print 'in from_json'
        print input_json
        self.name = input_json.get('name', self.name)
        user_json = input_json.get('user') # nested object / dict
        if user_json:
            print 'filtering user'
            self.user = User.filter_json(user_json) # just contains user fields
            print 'returned user is just none and throws no errors!: Problem!!!'
            print self.user
        # else:
        #     raise ValueError("TodoList.from_json: User Missing")

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

    # TODO update logic
    def put(self, id=None):
        pass

class TodoItemAPI(Resource):
    def get(self, listId, itemId):
        pass

# urls
# /user/<username>/list/<id>
# /user/<username>/list
# returns all lists for user
# /user/<username>/list/<listId>
# /user/<username>/list/<listId>/<itemId>
api.add_resource(UserAPI, '/user/<int:id>')
api.add_resource(UserListsAPI, '/user/<string:username>/todoLists')
api.add_resource(UserListsDeleteAPI, '/user/<string:username>/todoList/<int:listID>')
# below should only work with user verification
api.add_resource(TodoListsAPI, '/todoList')
api.add_resource(TodoListAPI, '/todoList/<int:listId>')
api.add_resource(TodoItemAPI, '/todoItem/<int:listId>/<int:itemId>')
app.register_blueprint(api_bp, url_prefix='/api')

def __initAdmin():
    # TODO
    # admin = User()
    db.session.add(admin)
    db.session.commit()
    print [user.id for user in User.query.all()]
    print User.query.filter_by(id=1).first()

def __initList():
    admin = User.query.filter_by(id=1).first()
    todoList = TodoList(name='Test List', user=admin)
    db.session.add(todoList)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    app.run()
