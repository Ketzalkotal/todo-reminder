var m = require('mithril');

module.exports = function(state){
    return {
        del: function(listID){
            return function(e){
                m.request({
                  method: "DELETE",
                  url: `api/user/${state.username}/todoList/${listID}`,
                }).then(function(result){
                    state.deleteList(listID);
                }).catch(alert);
            }
        },
        requestList:function(){
            m.request({
              method: "GET",
              url: `api/user/${state.username}/todoList`
            }).then(function(result){
              state.listItems = result;
            });
        },
        submit(e){
            m.request({
              method: "PUT",
              url: `api/user/${state.username}/todoList`,
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
              state.listItems.push({name: state.value, id: result.id}); // bad name
              state.value = "";
            });
        }
    };
};
