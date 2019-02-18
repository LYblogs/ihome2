function logout() {
    $.get("/user/logout", function(data){
        if (200 == data.code) {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.phone)
            $('#user-avatar').attr('src',data.data.avatar)
        },
        error:function(){
            console.log('error')
        }
    })
})