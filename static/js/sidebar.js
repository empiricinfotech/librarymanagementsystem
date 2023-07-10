$(document).ready(function () {
    $(".navbar-nav a").click(function () {
        $.each($(".navbar-nav a"), function( key, value ) {
            if (window.location.href == value){
              $(this).addClass("active");
            }
          });
    });
  });