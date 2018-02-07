var m = require('mithril');

var state = {
    username: "admin",
    value: "",
    setValue: function(v){
        state.value = v;
    },
    list: [],
    listItems: [],
    updateList: function(){
        this.list = this.listItems.map((item, index) => m(ListItem, {name: item.name, index: index}));
    },
    deleteList: function(index){
        console.log(`delete stub ${index}`);
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
      state.listItems.push({name: state.value});
      state.value = "";
    });
}

function del(index){
    return function(e){
        m.request({
          method: "DELETE",
          url: `api/${state.user}/todoList/${index}`,
        }).then(function(result){
            // TODO: delete it from state
            state.deleteList(index);
        }).catch(alert);
    }
}

var InputTodo = {
    view: function(vnode){
        return m('div', [
            m('input', {
                type: 'text',
                oninput: m.withAttr("value", state.setValue),
                onkeyup: function(e){ if(e.key === "Enter") submit(e) },
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
    // var listId = 1;
    var username = 'admin';
    m.request({
      method: "GET",
      url: `api/user/${username}/todoLists`
    }).then(function(result){
      state.listItems = result;
    });
  },
  view: function(vnode){
    state.updateList()
    return m('div', [
        m(InputTodo),
        m('ol', state.list)
    ])
  }
}
