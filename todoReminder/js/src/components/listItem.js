var m = require('mithril');
var AjaxWrapper = require('../Ajax');

module.exports = function(state){
    return {
        view: function(vnode){
            var Ajax = AjaxWrapper(state);
            return m('li',
                m('div', [
                    m('button.delete', {
                        onclick: Ajax.del(vnode.attrs.index),
                    }, 'X'),
                    m('a', {href: '#!/list'}, vnode.attrs.name),
                ])
            );
        }
    };
}
