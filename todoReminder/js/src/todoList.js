var m = require('mithril');
var state = require('./state');
var AjaxWrapper = require('./Ajax');
var Ajax = AjaxWrapper(state);

function failureMessage(message){
    alert(message);
}

var InputTodo = {
    view: function(vnode){
        return m('div', [
            m('input', {
                type: 'text',
                oninput: m.withAttr("value", state.setValue),
                onkeyup: function(e){ e.redraw = false; if(e.key === "Enter") Ajax.submit(e) },
                value: state.value,
            }),
            m('button', {
                type: 'submit',
                onclick: Ajax.submit
            }, 'Add')
        ]);
    }
}

module.exports = {
  oninit: function(vnode){
     Ajax.requestList();
  },
  view: function(vnode){
    state.updateList();
    return m('div', [
        m(InputTodo),
        m('ol', state.list)
    ])
  }
}
