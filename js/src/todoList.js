var m = require('mithril');

module.exports = {
  oninit: function(vnode){
    var listId = 1;
    m.request({
      method: "GET",
      url: `api/todoList/${listId}`,
    }).then(function(result){
      console.log('Then');
      console.log(result);
    }).catch(function(error){
      console.log('Error');
      console.log(error);
    });
  },
  view: function(){
    return m('ol', [
      m('li','one'),
      m('li','two'),
    ])
  }
}
