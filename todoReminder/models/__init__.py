from todoReminder import db
from user import User
from todoList import TodoList
from todoItem import TodoItem

def __initAdmin():
    admin = User(username="admin", email="admin@gmail.com")
    db.session.add(admin)
    db.session.commit()
    print [user.id for user in User.query.all()]
    print User.query.filter_by(id=1).first()

def __initList():
    admin = User.query.filter_by(id=1).first()
    todoList = TodoList(name='Test List', user=admin)
    db.session.add(todoList)
    db.session.commit()
