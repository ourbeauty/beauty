from django.conf.urls import url
from badmin import views

urlpatterns = [
    url(r'index/', views.index, name='aindex'),
    url(r'weclome/', views.weclome, name='aweclome'),
    url(r'syslog/', views.log, name='syslog'),
    url(r'changepass/', views.changepass, name='changepass'),
    url(r'charts7/', views.charts7, name='charts7'),
    url(r'charts6/', views.charts6, name='charts6'),
    url(r'charts5/', views.charts5, name='charts5'),
    url(r'charts4/', views.charts4, name='charts4'),
    url(r'charts3/', views.charts3, name='charts3'),
    url(r'charts2/', views.charts2, name='charts2'),
    url(r'charts1/', views.charts1, name='charts1'),
    url(r'alist/', views.alist, name='alist'),
    url(r'aper/', views.aper, name='aper'),
    url(r'arol/', views.arol, name='arol'),
    url(r'mlist/', views.mlist, name='mlist'),
    url(r'plist/', views.plist, name='plist'),
    url(r'pcate/', views.pcate, name='pcate'),
    url(r'olist/', views.olist, name='olist'),

    # 添加产品分类
    url(r'addcate/(?P<who>\d+)/(?P<num>\d+)/', views.addcate, name='addcate'),
    # 删除分类
    url(r'delcate/(?P<who>\d+)/(?P<num>\d+)/', views.delcate, name='delcate'),
    # 添加商品
    url(r'proadd/(?P<who>\d+)/(?P<num>\d+)/', views.addproduct, name='poradd'),
    # 获取商品分类
    url(r'getcate/', views.getcate, name='getcate'),
    # 删除商品
    url(r'delpro/(?P<num>\d+)/', views.delpro, name='delpro'),
    # 用户登录
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    # 获取验证码
    url(r'check_code/', views.set_code, name='checkcode'),

]
