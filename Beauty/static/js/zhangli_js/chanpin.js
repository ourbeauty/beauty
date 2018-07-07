function subShop() {
    // csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var number = $('#number1').text();

    $.ajax({
        url: '/App_zl/subgoods/',
        type: 'GET',
        data: {'number': number},
        // headers:{'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (msg) {
            if (msg.code == '200') {
                $('#number1').text(msg.number)
            }
            else {
                alert('只能是200以内的值')
            }
        },
        error: function () {
            alert('请求错误！')
        }
    });
    return false;
}


function addShop() {
    // 这里必须传入商品得id,说明是那个商品在购物车里得数据增加一
    // csrf = $('input[name="csrfmiddlewaretoken"]').val();  // 这里是解决csrf验证得问题
    var number = $('#number1').text();

    $.ajax({
        url: '/App_zl/addgoods/', // 通过那个函数方法来实现想要得方法
        type: 'GET',  // 请求类型
        // headers:{'X-CSRFToken': csrf}, // 解决csrf验证得问题
        data: {'number': number},  //这里是将页面传入的参数，返回到函数方法中。
        dataType: 'json',
        success: function (msg) {
            if (msg.code == '200') {

                $('#number1').text(msg.number)

            }
            else {
                alert('只能是200以内的值')
            }
        },
        error: function () {
            alert('请求错误！')
        }
    });
    return false;
}


function add_cart(id) {
    var number = $('#number1').text();
    var g_inventory= $('#g_inventory').text();

    // csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/App_zl/add_cart/',
        type: 'GET',
        data: {'id': id, 'number': number,'g_inventory':g_inventory},
        dataType: 'json',
        // headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            if (msg.code == '200') {

                location.href = '/App_zl/cart/'
            }
        },
        error: function () {
            alert('请求错误！')
        }
    });

}

function buy(id) {
    var number = $('#number1').text();
    var g_inventory= $('#g_inventory').text();
    // csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/App_zl/buy/',
        type: 'GET',
        data: {'id': id, 'number': number,'g_inventory':g_inventory},
        dataType: 'json',
        // headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            if (msg.code == '200') {

                location.href = '/App_zl/order/'
            }
        },
        error: function () {
            alert('请求错误！')
        }
    });

}