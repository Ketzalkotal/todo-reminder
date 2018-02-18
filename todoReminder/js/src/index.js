var m = require("mithril");
var Todos = require("./components/todoList");

m.route(document.body, "/todos", {
    "/todos": Todos,
})
