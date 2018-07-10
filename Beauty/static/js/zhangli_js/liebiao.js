function add_cart(id,code,g_inventory) {

    

    // csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/App_zl/add_one_cart/',
        type: 'GET',
        data: {'id': id,'g_inventory':g_inventory,'code':code},
        dataType: 'json',
        // headers: {'X-CSRFToken': csrf},
        success: function (msg) {

            if (msg.code == '200') {

                alert('商品添加成功！')
            }else if(msg.code='2000') {

                location.href='/App_yxr/login/?g_code='+msg.g_code+'&code='+msg.code
            }
            else{
                alert('商品库存不足！')
            }
        },
        error: function () {
            alert('请求错误！')
        }
    });

}