from django.conf.urls import url

from App import views

urlpatterns = [
    # url(r'^classify/$', views.classify, name='classify'),
    # url(r'^classify_list/(\d+)/$', views.classify_list, name='classify_list'),
    # url(r'^show/(\d+)/', views.show, name='show'),
    # url(r'^subgoods/',views.subgoods),
    # url(r'^addgoods/',views.addgoods),
    # url(r'^add_cart',views.add_cart),
    # url(r'^cart/',views.cart),
    # url(r'^buy/',views.buy,name='buy'),
    # url(r'^order/',views.order),

    url(r'adddizhi/$', views.adddizhi, name='adddizhi'),
    url(r'changedizhi/(?P<id>\d+)/$', views.changedizhi, name='changedizhi'),
    url(r'deldizhi/(\d+)/$', views.deldizhi, name='deldizhi'),
    url(r'dizhi/$', views.dizhi, name='dizhi')
]
