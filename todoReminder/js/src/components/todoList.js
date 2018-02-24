var m = require('mithril');
var state = require('../state');
var AjaxWrapper = require('../Ajax');
var Ajax = AjaxWrapper(state);

var InputTodo = {
    view: function(vnode){
        return m('div', {class: "ui segment"}, [
            m('div', {class: "ui fluid action huge input"}, [
                m('input', {
                    type: 'text',
                    oninput: m.withAttr("value", state.setValue),
                    onkeyup: function(e){ e.redraw = false; if(e.key === "Enter") Ajax.submit(e) },
                    value: state.value,
                }),
                m('div', {
                    onclick: Ajax.submit,
                    class: 'ui button'
                }, 'Add')
            ])
        ]);
    }
}

module.exports = {
  oninit: function(vnode){
     Ajax.requestList();
  },
  view: function(vnode){
    state.updateList();
    return m('div', {class: "main ui text container"}, [
        m(InputTodo),
        m('div', {class: 'ui relaxed middle aligned divided list'}, state.list)
    ])
  }
}
