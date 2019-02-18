function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$("#house-image").change(function(){
$("#house-avatar").attr("src",URL.createObjectURL($(this)[0].files[0]));
});

// 获取城区
$.ajax({
    type:"GET",
    url:"/home/house_info/",
    dataType:"json",
    success:function(data){
    var str =""
    for(i in data.data){
    str+="<option value="+data.data[i].id+">"+data.data[i].name+"</option>"
    }
    $('#area-id')[0].innerHTML =str

    },
    error:function(){
        consile.log('aaaa')

    }
})

//获取房屋配套设施
$.get('/home/house_facility/',function(data){
    for(i in data.data){
    $('#house_facility').append(
    '<li>'
        +'<div class="checkbox">'
        +'<label>'
        +'<input type="checkbox" name="facility" value="'+data.data[i].id+'">'+data.data[i].name
        +'</label>'
        +'</div>'
    +'</li>')
    };

})


$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $('#form-house-info').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
    url:'/home/my_newhouse/',
    type:'POST',
    dataType:'json',
    success:function(data){
        $('#form-house-info').attr('style','display:none')
        $('#form-house-image').attr('style','display:block')
        $('#house-id').val(data.data.house_id)

    },
    error:function(){
        console.log('error')

    }
    })
    })

    $('#form-house-image').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
    url:'/home/my_newhouse_img/',
    dataType:'json',
    type:'POST',
    success:function(data){
        console.log(data)

    },
    error:function(){
        console.log('error')

    }


    })

    })
})