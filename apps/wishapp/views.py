from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Product
import datetime

# Create your views here.
def additem(request):
	context = {
				'AuthorName': 'Henry Garmendia',
				'DateTime': datetime.datetime.now(),
		}
	return render(request, 'wishapp/additem.html', context)

def create_item(request):
	did_create = Product.objects.create_item(request);

	# if form success redirect to home page
	if did_create:
		return redirect('/dashboard') # this go back to success
	else:
		return redirect('/wish_items/create') # this go back to form

def single_item(request, id):

	context = {
			'AuthorName': 'Henry Garmendia',
			'DateTime': datetime.datetime.now(),
			'wish_items': Product.objects.get(id=id),
	}
	
	return render(request, 'wishapp/singleitem.html', context)