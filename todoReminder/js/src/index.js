var m = require("mithril");
var Todos = require("./todoList");

m.route(document.body, "/todos", {
    "/todos": Todos,
})
