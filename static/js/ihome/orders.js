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
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });
    $.get('/order/my_order_info/',function(data){
    console.log(data)
    for(i in data.data){
    $('.orders-list').append(
    '<li order-id=>'
                    +'<div class="order-title">'
                        +'<h3>订单编号：'+data.data[i].order_id+'</h3>'
                        +'<div class="fr order-operate">'
                            +'<button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>'
                        +'</div>'

                    +'</div>'
                    +'<div class="order-content">'
                        +'<img src="'+data.data[i].image+'">'
                        +'<div class="order-text">'
                            +'<h3>订单</h3>'
                            +'<ul>'
                                +'<li>创建时间：'+data.data[i].create_date+'</li>'
                                +'<li>入住日期：'+data.data[i].begin_date+'</li>'
                                +'<li>离开日期：'+data.data[i].end_date+'</li>'
                                +'<li>合计金额：'+data.data[i].amount+'元(共'+data.data[i].days+'晚)</li>'
                                +'<li>订单状态：'
                                    +'<span>'+data.data[i].status+'</span>'
                                +'</li>'
                                +'<li class="my_content">我的评价：'+data.data[i].comment+'</li>'
                                +'<li class="no_reason">拒单原因：'+data.data[i].comment+'</li>'
                            +'</ul>'
                        +'</div>'
                    +'</div>'
                +'</li>'

    )
    if(data.data[i].status!='待评价'){
        $('.order-operate').attr('style','display:none')

    }
    if(data.data[i].status!='已评价'){
        $('.my_content').attr('style','display:none')

    }
    if(data.data[i].status!='已拒单'){
        $('.no_reason').attr('style','display:none')

    }

    }

    })
});