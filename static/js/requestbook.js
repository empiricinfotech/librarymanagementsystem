function requestbook(e){
    var reqbook = document.getElementById('request_book'+e)
    var pendingbook = document.getElementById('pending_book'+e)
    $(reqbook).attr("hidden","true")
    pendingbook.removeAttribute("hidden");
}

function acceptbookrequest(e){
    document.getElementById('accept_'+e).onclick = function() { 
              name_Value=document.getElementById('book_name_'+e).value;
              $.ajax({
                  type: "POST",
                  url: "/viewallrequests/",
                  data: {
                      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                      bookid:e,
                      id:name_Value,
                  },
                  success: function(){
                      alert("Record Updated Successfully");
                      document.location = "/viewallrequests/"
                  },
                  error: function () {
                    alert("Unique Book No already Exists");
                    document.location = "/viewallrequests/"
                     }
            });
      }
}