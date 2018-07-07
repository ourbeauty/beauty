
from django.conf.urls import url, include

from App_zc import views

urlpatterns = [

    # 主页
    url(r'^index', views.Index, name='index'),

    # 搜索
    url(r'^search', views.search, name='search')
]