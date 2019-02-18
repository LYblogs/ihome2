function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    $(".book-house").show();

    $.get('/home/detail/',function(){
        r =window.location.search
        house_id =r.split('=')[1]
        x(house_id)
    })
    function x(){
    $.ajax({
        url:'/home/detail_info/',
        type:'GET',
        dataType:'json',
        data:{'house_id':house_id},
        success:function(data){
            console.log(data.data)
            for(i in data.data.images){
            $('.swiper-wrapper').append(
            '<li class="swiper-slide"><img src="'+data.data.images[i]+'"></li>'
            )
            }
            $('.house-title').text(data.data.title)
            $('.landlord-name span').text(data.data.user_name)
            $('#house_address').text(data.data.address)
            $('#house_count').append(
            '<h3>出租'+data.data.room_count+'间</h3>'
            +'<p>房屋面积:'+data.data.acreage+'平米</p>'
            +'<p>房屋户型:'+data.data.unit+'</p>'
            )
            $('#house_booking').attr('href','/order/booking/?house_id='+data.data.id)
            $('#user_image').attr('src',data.data.user_avatar)
            $('#house_man').text('宜住'+data.data.capacity+'人')
            $('#house_beds').text(data.data.beds)
            $('#house_deposit').text(data.data.deposit)
            $('#house_min').text(data.data.min_days)
            $('#house_max').text(data.data.max_days)
            $('.house-price span').text(data.data.price)
            for( i in data.data.facilities){
              $('#house_facility_list').append(
                '<li><span class="'+data.data.facilities[i].css+'"></span>'+data.data.facilities[i].name+'</li>'

              )

            }


            var mySwiper = new Swiper ('.swiper-container', {
                    loop: true,
                    autoplay: 2000,
                    autoplayDisableOnInteraction: false,
                    pagination: '.swiper-pagination',
                    paginationType: 'fraction'
                })

        },
        error:function(){
            console.log('error')

        }


    })
    }
})