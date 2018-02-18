var m = require('mithril');
var ListItemWrapper = require('./components/listItem');

var state = {
    username: "admin",
    value: "",
    setValue: function(v){
        state.value = v;
    },
    list: [], // m components
    listItems: [], // raw data: {name: str, id: int}
    schemas: {
        listItems:{
            name: "string",
            id: "number"
        },
    },
    deleteList: function(listID){
        state.listItems = state.listItems.filter(item => item.id !== listID);
    },
    updateList: function(){
        var ListItem = ListItemWrapper(state);
        state.list = state.listItems.map(item => m(ListItem, {name: item.name, index: item.id}));
    },
}
module.exports = state;
