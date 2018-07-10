from django.conf.urls import url

from cart import views
''
urlpatterns=[
    url(r'^user_cart/',views.user_cart,name='user_cart'),
    url(r'^cart/',views.cart,name='cart'),
    url(r'^cart_choice/',views.cart_choice,name='choice'),
    url(r'^cart_add_sub/',views.cart_add_sub,name='cart_add_sub'),
    url(r'^all_goods_cart/',views.all_goods_cart,name='all_goods_cart'),
    url(r'^order_settlement/',views.user_settlement,name='settlement'),
    url(r'^pay_page1',views.pay_page1,name='pay_page1'),
    url(r'^settlement1/',views.setlement1 ,name="settlement"),
    url(r'^user_settlement1/',views.user_settlement ,name="user_settlement"),
    # 支付完成 发送地址
    url(r'^pay_over/',views.pay_over,name='pay_over'),
    url(r'^all_create_order/',views.all_create_order,name='create_order'),
    url(r'^one_create_order/',views.one_create_order,name='one_create_order'),
    # 订单页面
    url(r'^order/',views.order,name='pay_order'),
    # 支付
    url(r'^immediately_pay/',views.immediately_pay,name='immediately_pay')
]