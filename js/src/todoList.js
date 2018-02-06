var m = require('mithril');

var state = {
    username: "admin",
    value: "",
    setValue: function(v){
        state.value = v;
    },
    list: [],
    listItems: []
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

var InputTodo = {
    view: function(vnode){
        return m('div', [
            m('input', {
                type: 'text',
                oninput: m.withAttr("value", state.setValue),
                value: state.value,
            }),
            m('button', {
                type: 'submit',
                onclick: submit
            }, 'Add')
        ]);
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
    state.list = state.listItems.map(item => m('li', item.name));
    return m('div', [
        m(InputTodo),
        m('ol', state.list)
    ])
  }
}
