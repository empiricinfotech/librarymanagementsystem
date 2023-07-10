function updateprofile()
{
    $(document.getElementById('update_profile')).attr("hidden","true")
    for(var i=0;i<document.getElementsByClassName("inputval").length;i++)
	document.getElementsByClassName("inputval")[i].removeAttribute('hidden');
    document.getElementById('done_edit').removeAttribute("hidden")
    $(document.getElementsByClassName("spandata")).attr("hidden","true")
}

function donechanges()
{

    $.ajax({
        method: "POST",
        url: "/profile/",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            first_name:document.getElementById('firstnm').value ,
            last_name:document.getElementById('lastnm').value ,
            username:document.getElementById('usernm').value ,
            email:document.getElementById('emailid').value ,
        },
        success: function(){
            alert("profile Updated Successfully");
            $(document.getElementById('done_edit')).attr("hidden","true")
            document.getElementById('update_profile').removeAttribute("hidden")
            $(document.getElementsByClassName("inputval")).attr("hidden","true")
            for(var i=0;i<document.getElementsByClassName("spandata").length;i++)
            document.getElementsByClassName("spandata")[i].removeAttribute('hidden');
            document.location = "/profile"
        
        },
        error: function () {
            alert("cant update");
            document.location = "/profile"
           }
    });

}