function is_choice(num, code) {
    var good_num = $('#num_' + num).html()
    $.ajax({
        url: '/cart/cart_choice',
        type: 'GET',
        data: {'g_id': num, 'code': code, 'good_num': good_num},
        dataType: 'json',
        success: function (data) {
            if (data.code == 200) {
                if (code) {
                    $('.is_chice_' + num).remove()
                    s = '<span class="is_chice_' + num + '" onclick="is_choice(' + num + ',false)">' +
                        '<span class="code2">×</span>' +
                        '</span>'
                    $('#chice_' + num).append(s)
                    var total = $('.fr .c_price').html()
                    var good = $('#num_' + num).html()
                    var price = $('#price_' + num).html().slice(2)
                    var mktprice = $('#mktprice_' + num).html().slice(2)
                    var totalmktprice = $('.container.nav-current-box.checkout-box .navbar-header>span').html().slice(6)
                    total = parseFloat(total) - parseFloat(price)
                    if (parseInt(good) != 0) {
                        totalmktprice = parseFloat(totalmktprice) - (parseFloat(mktprice) - parseFloat(price))
                    }
                    $('.fr .c_price').html(total)
                    $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(total)
                    $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省:￥' + totalmktprice)
                    $('#all_select').remove()
                    s = '<div class="confirm" id="all_select">\n' +
                        '<span class="is_choose" onclick="all_add_cart(' + 2 + ')"style="cursor:pointer">\n' +
                        '<span  >×</span>\n' +
                        '</span>'
                    $('.use_bouns.clearfix').append(s)
                } else {
                    $('.is_chice_' + num).remove()
                    s = '<span class="is_chice_' + num + '" onclick="is_choice(' + num + ',true)">' +
                        '<span class="code1">√</span>' +
                        '</span>'
                    $('#chice_' + num).append(s)
                    var total = $('.fr .c_price').html()
                    var good = $('#num_' + num).html()
                    var price = $('#price_' + num).html().slice(2)
                    var mktprice = $('#mktprice_' + num).html().slice(2)
                    var totalmktprice = $('.container.nav-current-box.checkout-box .navbar-header>span').html().slice(6)
                    total = parseFloat(total) + parseFloat(price)
                    totalmktprice = parseFloat(totalmktprice) + (parseFloat(mktprice) - parseFloat(price))
                    $('.fr .c_price').html(total)
                    $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(total)
                    $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省:￥' + totalmktprice)
                    if (typeof($('.code2')).html() == 'undefined') {
                        $('#all_select').remove()
                        s = '<div class="confirm" id="all_select">\n' +
                            '<span class="is_choose" onclick="all_del_cart(' + 1 + ')" style="cursor:pointer">\n' +
                            '<span  >√</span>\n' +
                            '</span>'
                        $('.use_bouns.clearfix').append(s)
                    }
                }
            }
        }
    })
    return false
};

function add_good(num) {
    $.ajax({
        url: '/cart/cart_add_sub',
        type: 'GET',
        data: {'good_id': num, 'status': 1},
        dataType: 'json',
        success: function (data) {
            if (data.code == 200) {
                var good_total = $('#price_' + num).html().slice(2)
                good_total = parseFloat(good_total) + parseFloat(data.good_price)
                $('#price_' + num).html('￥:' + good_total)
                var good_mktprice = $('#mktprice_' + num).html().slice(2)
                good_mktprice = parseFloat(good_mktprice) + parseFloat(data.good_mktprice)
                $('#mktprice_' + num).html('￥:' + good_mktprice)
                var page_num = parseInt($('#num_' + num).html()) + 1
                $('#num_' + num).html(page_num)
                if ($('.is_chice_' + num + '>span').html() == '√') {
                    var goods_total = $('.fr .c_price').html()
                    goods_total = parseFloat(goods_total) + parseFloat(data.good_price)
                    $('.fr .c_price').html(goods_total)
                    $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(goods_total)
                    var totalmktprice = $('.container.nav-current-box.checkout-box .navbar-header>span').html().slice(6)
                    totalmktprice = parseFloat(totalmktprice) + parseFloat(data.mkt_price)
                    $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省:￥' + totalmktprice)

                }
            }
        }
    })
    return false
};

function sub_good(num) {
    var page_num = parseInt($('#num_' + num).html())
    if (page_num > 0) {
        $.ajax({
            url: '/cart/cart_add_sub/',
            type: 'GET',
            data: {'good_id': num, 'status': 2},
            dataType: 'json',
            success: function (data) {
                if (data.code == 200) {
                    var good_total = $('#price_' + num).html().slice(2)
                    good_total = parseFloat(good_total) - parseFloat(data.good_price)
                    $('#price_' + num).html('￥:' + good_total)
                    var good_mktprice = $('#mktprice_' + num).html().slice(2)
                    good_mktprice = parseFloat(good_mktprice) - parseFloat(data.good_mktprice)
                    $('#mktprice_' + num).html('￥:' + good_mktprice)
                    var page_num = parseInt($('#num_' + num).html()) - 1
                    $('#num_' + num).html(page_num)
                    if ($('.is_chice_' + num + '>span').html() == '√') {
                        var goods_total = $('.fr .c_price').html()
                        goods_total = parseFloat(goods_total) - parseFloat(data.good_price)
                        $('.fr .c_price').html(goods_total)
                        $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(goods_total)
                        var totalmktprice = $('.container.nav-current-box.checkout-box .navbar-header>span').html().slice(6)
                        totalmktprice = parseFloat(totalmktprice) - parseFloat(data.mkt_price)
                        $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省:￥' + totalmktprice)

                    }
                }
            }
        })
        return false
    }
};

function all_del_cart(num) {
    if (parseInt(num) == 1) {
        $.ajax({
            url: '/cart/all_goods_cart',
            type: 'GET',
            data: {'status': num},
            datType: 'json',
            success: function (data) {
                if (data.code == 200) {
                    $('#all_select').remove()
                    s = '<div class="confirm" id="all_select">\n' +
                        '<span class="is_choose" onclick="all_add_cart(' + 2 + ')" style="cursor:pointer">\n' +
                        '<span  >×</span>\n' +
                        '</span>'
                    $('.use_bouns.clearfix').append(s)
                    for (good in data.goods) {
                        $('.is_chice_' + data.goods[good].g_id).remove()
                        s = '<span class="is_chice_' + data.goods[good].g_id + '" onclick="is_choice(' + data.goods[good].g_id + ',false)">' +
                            '<span class="code2">×</span>' +
                            '</span>'
                        $('#chice_' + data.goods[good].g_id).append(s)
                    }
                    $('.fr .c_price').html(0)
                    $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(0)
                    $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省:￥' + 0)
                }
            }
        })
        return false
    }
};

function all_add_cart(num) {
    var cart = {}
    $('.code2').parent().each(function () {
        var t = $(this).attr('class')
        var good_id = t.replace(/[^0,1,2,3,4,5,6,7,8,9]/g, '')
        var cart_num = $('#num_' + good_id).html()
        cart[good_id] = cart_num
    })
    if (parseInt(num) == 2) {
        $.ajax({
            url: '/cart/all_goods_cart',
            type: 'GET',
            data: {'status': num, 'carts_list': JSON.stringify(cart)},
            datType: 'json',
            success: function (data) {
                if (data.code == 200) {
                    $('#all_select').remove()
                    s = '<div class="confirm" id="all_select">\n' +
                        '<span class="is_choose" onclick="all_del_cart(' + 1 + ')"style="cursor:pointer" >\n' +
                        '<span  >√</span>\n' +
                        '</span>'
                    $('.use_bouns.clearfix').append(s)
                    for (good in data.goods) {
                        $('.is_chice_' + data.goods[good].g_id).remove()
                        s = '<span class="is_chice_' + data.goods[good].g_id + '" onclick="is_choice(' + data.goods[good].g_id + ',true)">' +
                            '<span class="code1">√</span>' +
                            '</span>'
                        $('#chice_' + data.goods[good].g_id).append(s)
                    }
                    var total = $('.container.nav-current-box.checkout-box .navbar-header>p>span').html()
                    var mkttotal = $('.container.nav-current-box.checkout-box .navbar-header>span').html().slice(6)
                    mkttotal = parseFloat(mkttotal) + parseFloat(data.mktprice)
                    total = parseFloat(total) + parseFloat(data.total)
                    $('.fr .c_price').html(total)
                    $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(total)
                    $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省:￥' + mkttotal)
                }
            }
        })

    }
};

$(document).ready(function () {
    $.ajax({
        url: '/cart/user_cart',
        type: 'GET',
        success: function (data) {
            if (data.code == 200) {
                for (good in data.goods) {
                    s = ' \n' +
                        '      <div class="cartlistinner clearfix" id="order_div_'+ data.goods[good].id+'">\n' +
                        '\t  \t<a href="" class="cart_orderlist_i">\n' +
                        '        \t<img style="display: inline;" src="' + data.goods[good].pic_url + '" data-original="//upload/merchandise/328791/MYTENO-MAG1143801660-5.jpg" data-onerror="//upload/merchandise/328791/MYTENO-MAG1143801660-5.jpg" data-brandlazy="true" height="101" width="80">\n' +
                        '\t\t</a>\n' +
                        '<div class="cart_orderlist_info"> <a href="//product-328791-43280703.html?rbc=url_cart">\n' +
                        ' <p class="cart_g_name">' + data.goods[good].g_name + '</p>\n' +
                        ' <p class="cart_b_name">' + data.goods[good].good_desc + '</p>\n' +
                        '                    <p class="fontgrey">颜色:' + data.goods[good].good_color + '</p>\n' +
                        '<p class="space5"></p>\n' +
                        '\t\t</a>\n' +
                        '  <div class="amount-confirm-box bord" data-product_id="43280703" data-size_id="112517730">\n' +
                        '<button class="amount-action amount-action-min " onclick="sub_good(' + data.goods[good].id + ')">-</button>' +
                        // '<a href="javascript:;" class="amount-action amount-action-min disabled" mars_sead="cart_edit_btn" data_mars="prd_id:43280703" onclick="sub_good('+data.goods[good].id+')">-</a>\n' +
                        '<span class="amount-text"id="num_' + data.goods[good].id + '">' + data.goods[good].cart_num + '</span>\n' +
                        '<input class="amount-num" readonly="readonly" data-brand-id="328791" data-product_id="43280703" data-size_id="112517730" data-id="" value="' + data.goods[good].cart_num + '" name="num" type="text">\n' +
                        // ' <a href="javascript:;" class="amount-action amount-action-max" data-action="addNum" mars_sead="cart_edit_btn" data_mars="prd_id:43280703" onclick="add_good('+data.goods[good].id+')">+</a>\n' +
                        '<button class="amount-action amount-action-max " onclick="add_good(' + data.goods[good].id + ')">+</button>' +
                        '          </div>\n' +
                        '        </div>\n' +
                        '       \t      <!--一般商品-->\n' +
                        '\t      <a class="cart_orderlist_p" href="" target="_blank" style="display:block">\n' +
                        '\t          <span class="c_price" id="price_' + data.goods[good].id + '">¥:' + data.goods[good].total + '</span>\n' +
                        '\t          <span class="fontstyle" id="mktprice_' + data.goods[good].id + '">¥:' + data.goods[good].mkttotal + '</span>\n' +
                        '\t      </a>\n' +
                        '\n' +
                        '\n' +
                        '    <span class="delete">\n' +
                        '       <a href="javascript:;" data-action="delete" data-usecoupon="0" mars_sead="cart_delect_btn" data_mars="prd_id:43280703">\n' +
                        '<div class="confirm" id="chice_' + data.goods[good].id + '" >' +
                        '<span class="is_chice_' + data.goods[good].id + '" onclick="is_choice(' + data.goods[good].id + ',true)">' +
                        '<span class="code1">√</span>' +
                        '</span>' +
                        '</div>' +
                        '</a>\n' +
                        '</span>\n' +
                        '</div>'+
                      '<div class="orderdeatilbox clearfix border_t" id="order_creat_div_'+ data.goods[good].id+'"  ><p class="qx_p">\n' +
                        '\t   <a class="dzf_quxiao_button" onclick="creat_oder('+data.goods[good].id +')">生成订单</a>\n' +
                          '\t   <a class="dzf_zhifu" onclick="one_order('+data.goods[good].id  +')">立即支付</a></p>\n' +
                        '\t</div>'
                    $('.cartlist.clearfix').append(s)

                }
                $('.fr .c_price').html(data.total)
                $('.container.nav-current-box.checkout-box .navbar-header>p>span').html(data.total)
                $('.container.nav-current-box.checkout-box .navbar-header>span').html('为您节省：￥' + data.mkttotal)
            }
        }
    })
    return false
});

function all_settelment() {
    var orders = {}
    $('.code1').parent().each(function () {
        var t = $(this).attr('class')
        var good_id = t.replace(/[^0,1,2,3,4,5,6,7,8,9]/g, '')
        var cart_num = $('#num_' + good_id).html()
        orders[good_id] = cart_num
    })
    if(Object.keys(orders).length >0) {
        $.ajax({
            url: '/cart/all_create_order/',
            type: 'GET',
            data: {'orders': JSON.stringify(orders)},
            dataType: 'json',
            success: function (data) {
                if (data.code == 200) {
                    url = '/cart/settlement1?&total=' + data.total_price + '&mkttotal=' + data.mkt_total_price
                    location.href = url

                }
            }
        })
        return
    }
}

function one_order(num) {
    var good_num = $('#num_' + num).html()
    if(parseInt(good_num)!=0) {
        $.ajax({
            url: '/cart/one_create_order',
            type: 'GET',
            data: {'g_id': num, 'g_num': good_num},
            success: function (data) {
                if (data.code == 200) {
                    url = '/cart/settlement1?&total=' + data.total_price + '&mkttotal=' + data.mkt_total_price
                    location.href = url
                }
            }
        })
        return false
    }
};
function creat_oder(num) {
    var good_num = $('#num_' + num).html()
    if(parseInt(good_num)!=0 ){
    $.ajax({
        url: '/cart/one_create_order',
        type: 'GET',
        data: {'g_id': num, 'g_num': good_num},
        success: function (data) {
            if (data.code == 200) {
            $('#order_div_'+num).remove()
            $('#order_creat_div_'+num).remove()
            }
        }
    })
        return false
        }
};






