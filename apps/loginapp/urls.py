from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.index),
    url(r'^login/register$', views.register),
    url(r'^login/login$', views.login),
    url(r'^login/logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_item_add$', views.wish_item_add),
    url(r'^remove$', views.remove),
    url(r'^delete', views.delete),
]