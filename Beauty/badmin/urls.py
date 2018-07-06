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
    url(r'ulist/', views.ulist, name='ulist'),
    url(r'plist/', views.plist, name='plist'),
    url(r'pcate/', views.pcate, name='pcate'),
    url(r'olist/', views.olist, name='olist'),
    url(r'madd/', views.madd, name='madd'),
    url(r'addadmin/', views.adminadd, name='adminadd')
]
