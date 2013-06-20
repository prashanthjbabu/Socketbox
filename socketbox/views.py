
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import urllib, urllib2
from django.utils import simplejson
import hashlib
from django.views.decorators.csrf import csrf_exempt
from socketbox.models import users,apps
import string,random
import json

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@csrf_exempt
def get_app_secret(request):
	if request.method=='POST' :
		if 'apikey' in request.POST :
			apikey=request.POST['apikey']
			myapp=apps.objects.filter(apikey=apikey)

			if len(myapp) == 0 :
				return_json_object = {
				'status' : 'invalidapikey',
				}
			else :
				secret=myapp[0].secret
				return_json_object = {
				'status' : 'success',
				'secret' : secret,
				}
			return_json_string = simplejson.dumps(return_json_object)
			return HttpResponse(return_json_string)


@csrf_exempt
def add_user(request):
	if request.method == 'POST' :
		if 'name' in request.POST and 'email' in request.POST and 'password' in request.POST :
			name=request.POST['name']
			email=request.POST['email']
			password=request.POST['password']
			password=hashlib.md5(password).hexdigest()

			user=users.objects.filter(email=email)

			if len(user) == 0: #user doesnt exist already
				new_user=users(name=name,email=email,password=password,activated=1)
				new_user.save() # add the user
				user=users.objects.filter(email=email)
				return_json_object = {
				'status' : 'success',
				'user_id' : user[0].id,
				}
			else : #user already exists
				return_json_object = {
				'status' : 'userexists',
				}

			

		else :
			return_json_object = {
				'status' : 'fieldsmissing',
				}
				
	else :
		return_json_object = {
				'status' : 'invalidpostrequest',
				}

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)

@csrf_exempt
def login_user(request):
	if request.method == "POST" :
		if 'email' in request.POST and 'password' in request.POST :
			email=request.POST['email']
			password=request.POST['password']
			password=hashlib.md5(password).hexdigest()
			return_text=validate_user(email,password)
			return HttpResponse(return_text)

def validate_user(email,password) :
	user=users.objects.filter(email=email)
	if len(user) == 0 :
		return_json_object = {
			'status' : 'userdoesnotexist',
		}
	else :
		if user[0].password == password :
			return_json_object = {
				'status' : 'success',
				'userid' : user[0].id,
				'name' : user[0].name,
			}
		else :
			return_json_object = {
				'status' : 'incorrectpassword',
			}
	
	return_json_string = simplejson.dumps(return_json_object)
	return return_json_string

def validate_user_inner(email,password) :
	user=users.objects.filter(email=email)
	if len(user) == 0 :
		status="userdoesnotexist"
	else :
		if user[0].password == password :
			status="success"
		else :
			status="incorrectpassword"	
	return status
def check_unique_apikey(apikey) :
	app=apps.objects.filter(apikey=apikey)
	if len(app) == 0 :
		return 1
	else :
		return 0

def check_unique_secret(secret) :
	app=apps.objects.filter(secret=secret)
	if len(app) == 0 :
		return 1
	else :
		return 0

@csrf_exempt
def show_apps(request):
	if request.method == "POST" :
		if 'email' in request.POST and 'password' in request.POST :
			email=request.POST['email']
			password=request.POST['password']
			password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			list_of_apps=[]
			if return_text== "success" :
				user=users.objects.filter(email=email)
				user_id=user[0].id
				myapps=apps.objects.filter(userid=user_id)
				return HttpResponse(serializers.serialize("json", myapps))
			else :
				return_json_object = {
				'status' : 'incorrectpassword',
				}
				return_json_string = simplejson.dumps(return_json_object)
				return HttpResponse(return_json_string)

@csrf_exempt
def rename_app(request):
	if request.method == "POST" :
		if 'email' in request.POST and 'password' in request.POST and 'oldappname' in request.POST and 'newappname' in request.POST :
			email=request.POST['email']
			password=request.POST['password']
			password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text== "success" :

				user=users.objects.filter(email=email)
				user_id=user[0].id
				old_app_name=request.POST['oldappname']
				new_app_name=request.POST['newappname']
				myapp=apps.objects.filter(userid=user_id).filter(appname=app_name)
				if len(myapp) == 0 :
					#invaild appname .. thats weird :P
					return_json_object = {
						'status' : 'invalidappname',
					}
				else :
					myapp.update(appname=new_app_name)
					return_json_object = {
						'status' : 'apprenamed',
					}
			else :
				return_json_object = {
						'status' : 'invalidlogin',
				}

			return_json_string = simplejson.dumps(return_json_object)
			return HttpResponse(return_json_string)


@csrf_exempt
def delete_app(request):
	if request.method == "POST" :
		if 'email' in request.POST and 'password' in request.POST and 'appname' in request.POST :
			email=request.POST['email']
			password=request.POST['password']
			password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text== "success" :

				user=users.objects.filter(email=email)
				user_id=user[0].id
				app_name=request.POST['appname']

				myapp=apps.objects.filter(userid=user_id).filter(appname=app_name)
				if len(myapp) == 0 :
					#invaild appname .. thats weird :P
					return_json_object = {
						'status' : 'invalidappname',
					}
				else :
					myapp.delete()
					return_json_object = {
						'status' : 'appdeleted',
					}
			else :
				return_json_object = {
						'status' : 'invalidlogin',
				}

			return_json_string = simplejson.dumps(return_json_object)
			return HttpResponse(return_json_string)


@csrf_exempt
def create_app(request):
	if request.method == "POST" :
		if 'email' in request.POST and 'password' in request.POST and 'appname' in request.POST :
			email=request.POST['email']
			password=request.POST['password']
			password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text== "success" :

				user=users.objects.filter(email=email)
				user_id=user[0].id
				app_name=request.POST['appname']

				myapp=apps.objects.filter(userid=user_id).filter(appname=app_name)
				if len(myapp) == 0 :
					#create the app no duplicates
					#check if apikey is unique
					while True :
						apikey=random_generator(10)
						if check_unique_apikey(apikey) == 1 :
							break

					
					secret=random_generator(10)
					#check if secret is unique
					while True :
						secret=random_generator(10)
						if check_unique_secret(secret) == 1 :
							break
					
					new_app=apps(userid=user_id,appname=app_name,secret=secret,apikey=apikey)
					new_app.save() # add the user
					return_json_object = {
						'status' : 'appcreated',
						'secret' : secret,
						'apikey' : apikey,
						'appname' : app_name,
					}
		
				else :
					#app name already exists
					return_json_object = {
						'status' : 'appnameexists',
					}

			else :
				return_json_object = {
						'status' : 'invalidlogin',
				}

			return_json_string = simplejson.dumps(return_json_object)
			return HttpResponse(return_json_string)

def sock_test(request):
	event = "hello"
	apikey="BU4IBO0JTE"
	secret="XDZK7RMAC3ww"
	channel = "prash"
	data = {
		'name' : 'Prashanth',
		'age' : '21',
	}
	socket_data = {
		'event' : event,
		'channel' : channel,
		'data' : simplejson.dumps(data),
		'apikey' : apikey,
		'secret' : secret,
	}

	host = 'http://socketbox.insigniadevs.com:8000';
	try:
		result = urllib2.urlopen(host + '/post/', urllib.urlencode(socket_data))
		content = result.read()
	except Exception:
		content = "FAIL"
	return HttpResponse(content)