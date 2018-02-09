var m = require('mithril');

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
    updateList: function(){
        state.list = state.listItems.map(item => m(ListItem, {name: item.name, index: item.id}));
    },
    deleteList: function(listID){
        state.listItems = state.listItems.filter(item => item.id !== listID);
    },
    requestList:function(){
        var username = 'admin';
        m.request({
          method: "GET",
          url: `api/user/${username}/todoLists`
        }).then(function(result){
          state.listItems = result;
        });
    }
}

function failureMessage(message){
    alert(message);
}

function submit(e){
    m.request({
      method: "PUT",
      url: 'api/todoList',
      headers: {
          'Content-Type': 'application/json'
      },
      data: {
          user: {
              username: state.username
          },
          name: state.value
      }
    }).then(function(result){
      state.listItems.push({name: state.value, id: result.id}); // bad name
      state.value = "";
    });
}

function del(listID){
    return function(e){
        m.request({
          method: "DELETE",
          url: `api/user/${state.username}/todoList/${listID}`,
        }).then(function(result){
            state.deleteList(listID);
        }).catch(alert);
    }
}

var InputTodo = {
    view: function(vnode){
        return m('div', [
            m('input', {
                type: 'text',
                oninput: m.withAttr("value", state.setValue),
                onkeyup: function(e){ e.redraw = false; if(e.key === "Enter") submit(e) },
                value: state.value,
            }),
            m('button', {
                type: 'submit',
                onclick: submit
            }, 'Add')
        ]);
    }
}

var ListItem = {
    view: function(vnode){
        return m('li',
            m('div', [
                m('button.delete', {
                    onclick: del(vnode.attrs.index),
                }, 'X'),
                vnode.attrs.name,
            ])
        );
    }
}

module.exports = {
  oninit: function(vnode){
      state.requestList();
  },
  view: function(vnode){
    state.updateList()
    return m('div', [
        m(InputTodo),
        m('ol', state.list)
    ])
  }
}
