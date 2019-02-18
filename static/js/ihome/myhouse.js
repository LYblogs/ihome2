$(document).ready(function(){
    $.ajax({
    url:'/home/is_auth/',
    dataType:'json',
    type:'GET',
    success:function(data){
        if(data.code !=200){
        $(".auth-warn").show();
        }
    },
    error:function(){
        console.log('error')
    }

    })
    $.get('/home/myhouse_info/',function(data){
        for(i in data.data){
        $('#houses-list').append(
                '<li>'
                    +'<a href="/home/detail/?house_id='+data.data[i].id+'">'
                        +'<div class="house-title">'
                            +'<h3>房屋ID:'+data.data[i].id+'—— '+data.data[i].title+'</h3>'
                        +'</div>'
                        +'<div class="house-content">'
                            +'<img src="'+data.data[i].image+'">'
                            +'<div class="house-text">'
                                +'<ul>'
                                    +'<li>位于：'+data.data[i].area+'</li>'
                                    +'<li>价格：￥'+data.data[i].price+'/晚</li>'
                                    +'<li>发布时间：'+data.data[i].create_time+'</li>'
                                +'</ul>'
                            +'</div>'
                        +'</div>'
                    +'</a>'
                +'</li>'
        )

        }


    })


})