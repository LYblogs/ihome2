function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    house1=window.location.search
    house_id=house1.split('=')[1]
    $.ajax({
        url:'/home/detail_info/',
        type:'GET',
        dataType:'json',
        data:{'house_id':house_id},
        success:function(data){
        console.log(data)
        $('.house-info img').attr('src',data.data.images[0])
        $('#house_text').append(
            '<h3>'+data.data.title+'</h3>'
            +'<p>￥<span id="one_price">'+data.data.price+'</span>/晚</p>'

        )

        },
        error:function(){
        console.log('error')
        }


    })
    $('#submit_order').click(function(){
     start_date = $('#start-date').val()
     end_date = $('#end-date').val()
     order_price=$('#order_price').text()
     one_price=$('#one_price').text()
     $.ajax({
     url:'/order/booking/',
     type:'POST',
     dataType:'json',
     data:{'start_date':start_date,'end_date':end_date,'order_price':order_price,'one_price':one_price,'house_id':house_id},
     success:function(data){
     location.href='/order/my_order/'

     },
     error:function(){
     console.log('error')
     }
     })


    })

})
