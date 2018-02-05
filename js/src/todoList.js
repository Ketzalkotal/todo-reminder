var m = require('mithril');

var list = [];

module.exports = {
  oninit: function(vnode){
    // var listId = 1;
    var username = 'admin';
    m.request({
      method: "GET",
      url: `api/user/${username}/todoLists`
    }).then(function(result){
      list = result.map(item => m('li', item.name));
    }).catch(function(error){
      console.log(error);
    });
  },
  view: function(){
    return m('ol', list)
  }
}
