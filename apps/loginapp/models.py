from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from datetime import datetime, timedelta
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
ALPHA_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX1 = re.compile(r'.*?\d') # .*?\d    checks for at least one digit
PASSWORD_REGEX2 = re.compile(r'.*?[A-Z]') # .*?[A-Z] checks for at least one uppercase letter
PASSWORD_REGEX3 = re.compile(r'.*?[a-z]') # .*?[a-z] checks for at least one lowercase letter
# PASSWORD_REGEX4 = re.compile(r'.*?[\$\!\?\%\&]') # .*?[!?%&_] checks for at least one special character

# Create your models here.
class UserManager(models.Manager):
	"""docstring for UserManager"""
	def register(self, request):

		is_valid = True
		# get the values from the form
		# validate the form
		if len(request.POST['full_name']) == 0:
			messages.error(request, 'Your full name is required!', extra_tags='full_name')
			is_valid = False;

		elif len(request.POST['full_name']) < 3:
			messages.error(request, 'Must be at least 3 characters!', extra_tags='full_name')
			is_valid = False;

		if len(request.POST['email']) < 0:
			messages.error(request, 'Please provide email!', extra_tags='email')
			is_valid = False;

		# make sure the email is not already in use
		clean_email = User.objects.filter(email=request.POST['email'])

		if len(clean_email) > 0:
			messages.error(request, 'That email already exists!')
			is_valid = False;

		elif not EMAIL_REGEX.match(request.POST['email']):
			messages.error(request, 'Not a valid email', extra_tags='email')
			is_valid = False;

		if len(request.POST['password']) < 0:
			messages.error(request, 'Cannot be blank!', extra_tags='password')
			is_valid = False;

		elif len(request.POST['password']) < 8:
			messages.error(request, 'Must be at least 8 characters', extra_tags='password')
			is_valid = False;

		elif not PASSWORD_REGEX1.match(request.POST['password']):
			messages.error(request, 'Must contain at least 1 number', extra_tags='password')
			is_valid = False;

		elif not PASSWORD_REGEX2.match(request.POST['password']):
			messages.error(request, 'Must contain at least 1 Uppercas letter', extra_tags='password')
			is_valid = False;

		elif not PASSWORD_REGEX3.match(request.POST['password']):
			messages.error(request, 'Must contain at least 1 lowercase letter', extra_tags='password')
			is_valid = False;

		# elif not PASSWORD_REGEX4.match(request.POST['password']):
		# 	messages.error(request, 'Password must contain at least 1 special character i.e. !$?%&')
		# 	is_valid = False;

		elif request.POST['password'] != request.POST['password_confirm']:
			messages.error(request, 'Password do not match!', extra_tags='password_confirm')
			is_valid = False;

		elif request.POST['datehired'] < 0:
			messages.error(reques, 'Please provide a date', extra_tags='datehired')
			is_valid = False;

		if not is_valid:
			return False

		# hash the password
		hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())

		# put in database
		new_user = User(
				full_name = request.POST['full_name'],
				email = request.POST['email'],
				pwhash = hashed,
				datehired = request.POST['datehired'],

			)
		# save the new user
		new_user.save()

		# set the new login user in session
		request.session['logged_in_user'] = new_user.id 

		return True

	def login(self, request):
		# validation goes here
		if request.POST['email'] < 0 or request.POST['password'] < 0:
			messages.error(request, 'Make sure email and password fields are filled in.', extra_tags='logemail')

		# does the user exits?
		users = User.objects.filter(email=request.POST['email'])

		if len(users) == 0:
			messages.error(request, 'That user does not exist', extra_tags='logemail')
			return False

		user = users[0]
		# does the hash match?
		hashed3 = bcrypt.hashpw(request.POST['password'].encode('utf-8'), user.pwhash.encode('utf-8'))

		if hashed3 != user.pwhash:
			messages.error(request, 'That password is incorrect', extra_tags='logpassword')
			return False

		# set the login user id in the session
		request.session['logged_in_user'] = user.id 

		return True

class User(models.Model):
	"""docstring for User"""
	full_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	pwhash = models.CharField(max_length=255)
	datehired = models.DateTimeField(default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# we are overwriting the object with our own object
	objects = UserManager()
		