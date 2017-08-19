from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$',views.login, name="login"),
    url(r'^friendpage$', views.friendpage, name="friendpage"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^users/add/(?P<id>\d+)$', views.add_friend),
    url(r'^users/unfriend/(?P<id>\d+)$', views.unfriend),
    url(r'^users/(?P<id>\d+)$', views.profile),

]