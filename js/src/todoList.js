var m = require('mithril');

module.exports = {
  view: function(){
    return m('ol', [
      m('li','one'),
      m('li','two'),
    ])
  }
}
