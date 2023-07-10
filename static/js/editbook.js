function datachange(e){
  var editbtn = document.getElementById('update_pen'+e)
  var donebtn = document.getElementById('edit_data'+e)
  var nameSpan = document.getElementById('span_name_'+e)
  var authorSpan = document.getElementById('span_author_'+e)
  var bookNoSpan = document.getElementById('span_bookno_'+e)
  var qtySpan = document.getElementById('span_qty_'+e)
  var name=document.getElementById('book_name_'+e);
  var author=document.getElementById('book_author_'+e);
  var bookno=document.getElementById('book_No_'+e);
  var qty=document.getElementById('book_qty_'+e);
  $(editbtn).attr("hidden","true")
  $(nameSpan).attr("hidden","true")
  $(authorSpan).attr("hidden","true")
  $(bookNoSpan).attr("hidden","true")
  $(qtySpan).attr("hidden","true")
  donebtn.removeAttribute("hidden");
  name.removeAttribute("hidden");
  author.removeAttribute("hidden");
  bookno.removeAttribute("hidden");
  qty.removeAttribute("hidden");
}

function postchange(e){
var editbtn = document.getElementById('update_pen'+e)
var donebtn = document.getElementById('edit_data'+e)
var name=document.getElementById('book_name_'+e);
var author=document.getElementById('book_author_'+e);
var bookno=document.getElementById('book_No_'+e);
var qty=document.getElementById('book_qty_'+e);
        name_Value=document.getElementById('book_name_'+e).value;
        author_Value=document.getElementById('book_author_'+e).value;
        bookno_Value=document.getElementById('book_No_'+e).value;
        qty_Value=document.getElementById('book_qty_'+e).value;
        $.ajax({
            type: "POST",
            url: "/listbooks/",
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                bookid:e,
                booknm:name_Value,
                authornm:author_Value,
                booknumber:bookno_Value,
                qtys:qty_Value,
            },
            success: function(){
                alert("Record Updated Successfully");
                $(donebtn).attr("hidden","true")
                $(name).attr("hidden","true");
                $(author).attr("hidden","true");
                $(bookno).attr("hidden","true");
                $(qty).attr("hidden","true");
                document.getElementById('update_pen'+e).removeAttribute("hidden");
                document.getElementById('span_name_'+e).removeAttribute("hidden");
                document.getElementById('span_author_'+e).removeAttribute("hidden");
                document.getElementById('span_bookno_'+e).removeAttribute("hidden");
                document.getElementById('span_qty_'+e).removeAttribute("hidden");
                document.location = "/listbooks/"
            },
            error: function () {
                alert("Unique Book No already Exists");
                document.location = "/listbooks/"
               }
      });


} 