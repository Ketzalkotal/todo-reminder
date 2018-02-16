var m = require("mithril");
var TodoList = require("./todoList");

m.route(document.body, "/todo", {
    "/todo":  TodoList,
})
