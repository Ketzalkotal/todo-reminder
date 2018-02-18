# todo-reminder
A todo app that creates reminders through Google Calendar.

## Dev Server
```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
Run as a module
```sh
python -m todoReminder.main
```
Or through flask
```sh
source VARS.sh
flask todoReminder/main.py
```

## Javascript
```sh
cd js
npm install
npm run start
```

## Lazy Man's Graphql
to_json is a helper method defined in the models to allow you to quickly serialize Models.

filter_json allows you to create Rows with relations by including query statements in the PUT request JSON.

### Examples

#### Schema
```csv
Users
id, username, email
---
1,"admin","admin@todoreminder.com"
```

Given this schema, the following PUT requests would both create "Admin's Todo List" rows and associate them with the admin user in a single query.

```JSON
{
	"user": {
		"username": "admin"
	},
	"name": "Admin's Todo List"
}
```
```JSON
{
	"user": {
		"email": "admin@todoreminder.com"
	},
	"name": "Admin's Todo List"
}
```

## Possible Issues

### Lazy Man's Graphql Problems

The to_json helper method may need to be able to detect circular references, because relations may model graphs rather than trees.

We could pass a context that holds enough information to detect these circular references, or we could explicitly limit depth when following to_json methods recursively.
