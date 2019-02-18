function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $.ajax({
    url:'/user/auth_info/',
    type:'GET',
    dataType:'json',
    success:function(data){
        $('#real-name').val(data.data.id_name)
        $('#id-card').val(data.data.id_card)
        if(data.code ==1011){
        $('#real-name').attr('disabled','disabled')
        $('#id-card').attr('disabled','disabled')
        $('#save_auth').css('display','none')
        }
    },
    error:function(){
        console.log('error')
    }

    })

    $('#form-auth').submit(function(e){
    e.preventDefault();
    var iname=$('#real-name').val()
    var icard =$('#id-card').val()
    $.ajax({
        url:'/user/auth/',
        type:'POST',
        dataType:'json',
        data:{'iname':iname,'icard':icard},
        success:function(data){
            console.log(data)
            if(data.code != 200){
            $('.error-msg').html(data.msg)
            $('.error-msg').show()
            }
            if(data.code == 200){
            location.href='/user/my/'
            }

        },
        error:function(){
            console.log('error')
        }

    })

    })

})