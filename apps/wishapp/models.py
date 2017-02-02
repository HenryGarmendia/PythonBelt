from __future__ import unicode_literals
from django.contrib import messages
from django.db import models

from ..loginapp.models import User
# Create your models here.

class ItemManager(models.Manager):
	"""docstring for ItemManager"""
	def create_item(self, request):
		# validation the product
		is_valid = True;

		if len(request.POST['itemName']) == 0:
			messages.error(request, 'Product name is required!', extra_tags='itemName')
			is_valid = False

		if len(request.POST['itemName']) < 3:
			messages.error(request, 'Product name must be at least 3 characters!', extra_tags='itemName')
			is_valid = False

		if not is_valid:
			# if validation is falls
			return False;

		user = User.objects.get(id=request.session['logged_in_user'])

		# graving the form field and creating a item 
		wish_item = Product.objects.create(
			itemName=request.POST['itemName'], 
			created_by=user,
			)
		
		# saving the item to the db
		# wish_item.wished_by.add(user)
		wish_item.save()

		# return True if everything gose well
		return True

class Product(models.Model):
	"""docstring for Product"""
	itemName = models.CharField(max_length=100)
	created_by = models.ForeignKey(User, related_name='created_items')
	wished_by = models.ManyToManyField(User, related_name='wish_list')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ItemManager()