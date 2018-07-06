from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'adddizhi/$', views.adddizhi, name='adddizhi'),
    url(r'changedizhi/(?P<id>\d+)/$', views.changedizhi, name='changedizhi'),
    url(r'deldizhi/(\d+)/$', views.deldizhi, name='deldizhi'),
    url(r'dizhi/$', views.dizhi, name='dizhi')
]