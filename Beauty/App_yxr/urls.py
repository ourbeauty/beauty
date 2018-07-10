from django.conf.urls import url

from App_yxr import views

urlpatterns = [
    # 登录
    url(r'^login/',views.login, name='login'),
    # 注册
    url(r'^regist/',views.register,name='regist'),
    # 个人中心
    url(r'^user/',views.user,name='user'),
    # 注销
    url(r'^logout/',views.logout,name='logout'),

    # 更多订单
    url(r'^allorders/',views.allorders,name='allorders'),
    # 待支付
    url(r'^WaitPay/',views.wait_pay,name='WaitPay'),
    # 待收货
    url(r'^EndPay/',views.end_pay,name='EndPay'),


]




