var m = require('mithril');
var AjaxWrapper = require('../Ajax');

module.exports = function(state){
    return {
        view: function(vnode){
            var Ajax = AjaxWrapper(state);
            return m('div', {class: "item"}, [
                m('div', {class: "right floated content"}, [
                    m('div', {
                        onclick: Ajax.del(vnode.attrs.index),
                        class: "ui right floated red small button"
                    }, 'X'),
                ]),
                m('div', {class: "content"}, [
                    m('h3', vnode.attrs.name),
                ]),
            ]);
        }
    };
}
