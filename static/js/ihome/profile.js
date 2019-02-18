function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$("#img_input").change(function(){
$("#user-avatar").attr("src",URL.createObjectURL($(this)[0].files[0]));
});



$(document).ready(function() {
    $('#form-avatar').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/profile/',
            type:'PATCH',
            dataType:'json',
            success:function(data){

            console.log(data)
            },
            error:function(){
            console.log('error')
            }
        })
    });
    $('#form-name').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
            url:'/user/profile/',
            type:'PATCH',
            dataType:'json',
            success:function(data){
            console.log(data)
            },
            error:function(){
            console.log('error')
            }
        })
    })


    })

