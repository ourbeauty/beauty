from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'dizhi/', views.dizhi, name='dizhi'),
    url(r'adddizhi/', views.adddizhi, name='adddizhi')
]