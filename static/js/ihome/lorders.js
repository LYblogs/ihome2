//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/order/other_order_info/',function(data){
        console.log(data)
        for(i in data.data){
        $('.orders-list').append(
        '<li order-id='+data.data[i].order_id+'>'
                    +'<div class="order-title">'
                        +'<h3>订单编号：'+data.data[i].order_id+'</h3>'
                        +'<div class="fr order-operate">'
                            +'<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal">接单</button>'
                            +'<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal">拒单</button>'
                        +'</div>'
                    +'</div>'
                    +'<div class="order-content">'
                        +'<img src="'+data.data[i].image+'">'
                        +'<div class="order-text">'
                            +'<h3>'+data.data[i].house_title+'</h3>'
                            +'<ul>'
                                +'<li>创建时间：'+data.data[i].create_date+'</li>'
                                +'<li>入住日期：'+data.data[i].begin_date+'</li>'
                                +'<li>离开日期：'+data.data[i].end_date+'</li>'
                                +'<li>合计金额：￥'+data.data[i].amount+'(共'+data.data[i].days+'晚)</li>'
                                +'<li>订单状态：'
                                    +'<span>'+data.data[i].status+'</span>'
                                +'</li>'
                                +'<li class="other_content"id="other_content_'+data.data[i].order_id+'">客户评价：'+ data.data[i].comment+'</li>'
                            +'</ul>'
                        +'</div>'
                    +'</div>'
                +'</li>'


        )
        if(data.data[i].status !='待接单'){
        $('.order-operate').attr('style','display:none')

        }
        if(data.data[i].status !='已评价'){
        $('#other_content_'+data.data[i].order_id).attr('style','display:none')

        }
        if(data.data[i].status == '已拒单'){
        $('#other_content_'+data.data[i].order_id).attr('style','display:block')
        $('#other_content_'+data.data[i].order_id).text('拒单原因：'+data.data[i].comment)
        console.log($('#other_content_'+data.data[i].order_id).text())
        }


        }
        $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        console.log(orderId)
        $(".modal-reject").attr("order-id", orderId);
    });

    })
    $('.modal-accept').on("click",function(){
    my_id= $('.modal-accept').attr('order-id')
    console.log(my_id)
    $.ajax({
       url:'/order/order_status/',
       type:'POST',
       dataType:'json',
       data:{'my_status':'WAIT_PAYMENT','my_id':my_id},
       success:function(data){
            location.href='/order/other_order/'
       },
       error:function(){
       console.log('error')

       }



    })


    })

    $('.modal-reject').on("click",function(){
    my_id= $('.modal-reject').attr('order-id')
    order_comment = $('#reject-reason').val()
    console.log(order_comment)
    $.ajax({
       url:'/order/order_status/',
       type:'POST',
       dataType:'json',
       data:{'my_status':'REJECTED','my_id':my_id,'order_comment':order_comment},
       success:function(data){
            location.href='/order/other_order/'
       },
       error:function(){
       console.log('error')

       }



    })


    })


});