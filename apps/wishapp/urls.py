from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create$', views.additem), # to the home page of additem/create 
	url(r'^createItem$', views.create_item), # to create a item to the list
	url(r'^singleitem/(?P<id>\d+)$', views.single_item), # to the single item page
]