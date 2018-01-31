var m = require('mithril');

module.exports = {
  oninit: function(vnode){
    m.request({
      method: "GET",
      url: "api/todoList",
    }).then(function(result){
      console.log(result);
    });
  },
  view: function(){
    return m('ol', [
      m('li','one'),
      m('li','two'),
    ])
  }
}
