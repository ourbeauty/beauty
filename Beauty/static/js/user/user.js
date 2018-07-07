$(document).ready(function(){

    $.get('/user/user/',function (data) {
        if(data.code=='200'){
            $('#username').html(data.u_name);
        }

    })
});

