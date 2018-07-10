//
// $(document).ready(function () {
//     $.ajax({
//         url:'/cart/order_settlement/',
//         type:'GET',
//         success:function (data) {
//             if(data.code==200){
//                 $('.u-name').html(data.order.name)
//                 $('.u-address').html(data.order.addr)
//                 $('.nav.nav-list-totle >li:first >span').html('￥'+data.order.total_price)
//                 $('.nav.nav-list-totle >li:last >span').html('￥'+data.order.total_price)
//                 $('.navbar-header .totle .price').html(data.order.total_price)
//                 $('.navbar-header > span').html('为您节省：¥'+data.order.mktprice)
//             }
//         }
//
//     })
//     return false
// })

$(document).ready(function () {
    var status=window.location.search
    var total =status.match(/\d+/g)[0]
    var mkttotal =status.match(/\d+/g)[1]
    if(status.length>0){
        $.ajax({
            url:'/cart/user_settlement1',
            type:'GET',
            success:function (data) {
                if(data.code==200){
                    $('.u-name').html(data.order.name)
                $('.u-address').html(data.order.addr)
                $('.nav.nav-list-totle >li:first >span').html('￥'+total)
                $('.nav.nav-list-totle >li:last >span').html('￥'+total)
                $('.navbar-header .totle .price').html(total)
                $('.navbar-header > span').html('为您节省：¥'+mkttotal)
                }
            }
        })
    }

})











