from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.timezone import activate

from ..wishapp.models import Product
from .models import User
import datetime

# Create your views here.
def index(request):
	context = {
			'AuthorName': 'Henry Garmendia',
			'DateTime': datetime.datetime.now()
	}

	return render(request, 'loginapp/index.html', context)

def register(request):
	did_register = User.objects.register(request)

	if did_register:
		users = User.objects.get(email=request.POST['email'])

		return redirect('/dashboard')
	else:
		return redirect('/')

def login(request):
	did_login = User.objects.login(request)

	if did_login:
		users = User.objects.get(email=request.POST['email'])

		return redirect('/dashboard')
	else:
		return redirect('/login')

def logout(request):
	request.session['logged_in_user'] = 0

	return redirect('/')

def dashboard(request):
	# puts the user in session
	user = User.objects.get(id=request.session['logged_in_user'])

	# go to the DB and grab the items for the user in the session
	wish_items = Product.objects.filter(wished_by=user)

	# this will display other users items in the table
	other_wish_items = Product.objects.exclude(wished_by=user)

	context = {
			'AuthorName': 'Henry Garmendia',
			'DateTime': datetime.datetime.now(),
			'users': user,
			'user_wish_list': wish_items,
			'other_wish_list': other_wish_items,
	}

	return render(request, 'loginapp/dashboard.html', context)

def wish_item_add(request):
	# puts the user in session
	user = User.objects.get(id=request.session["logged_in_user"])

	# item = Product.objects.get(id = id)

	wish_item = Product.objects.get(id=request.POST["wish_item_id"])

	user.wish_list.add(wish_item)
	user.save()

	return redirect('/dashboard')

def remove(request):
	# puts the user in session
	user = User.objects.get(id=request.session["logged_in_user"])

	wish_item = Product.objects.get(id=request.POST["wish_item_id"])

	user.wish_list.remove(wish_item)
	user.save()

	return redirect("/dashboard")

def delete(request):
	
    wish_item = Product.objects.get(id=request.POST["wish_item_id"])
    wish_item.delete();

    return redirect("/dashboard")



































