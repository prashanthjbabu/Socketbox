
# Create your views here.
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.db.models import Count
import urllib, urllib2
from django.utils import simplejson
import hashlib
from django.views.decorators.csrf import csrf_exempt
from socketbox.models import users,apps,stats
from django.core.mail import send_mail
from django.template import RequestContext

import string,random,datetime
import json
from django.utils import timezone

timezone.activate('Asia/Calcutta')


def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@csrf_exempt
def edit_account(request) :
	if request.method == "POST" :
		if 'name' in request.POST and 'password' in request.POST and 'newpassword' in request.POST :
			name=request.POST['name']
			password=request.POST['password']
			newpassword=request.POST['newpassword']
			email=request.session['email']
			myuser=users.objects.filter(email=email)
			if myuser[0].password == password :
				#auth success , proceed to update profile
				myuser.update(password=newpassword,name=name)
				return_json_object = {
					'status' : 'success',
				}
			else :
				return_json_object = {
					'status' : 'incorrectpassword',
				}
		else :
			return_json_object = {
				'status' : 'invalidpostrequest',
			}
	else :
		return_json_object = {
			'status' : 'invalidpostrequest',
		}	

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)	

@csrf_exempt
def account(request):
	if 'user_id' in request.session :
		#session exists for user
		userid=request.session['user_id']
		myapps=apps.objects.filter(userid=userid)
		mydetails=users.objects.filter(id=userid)
		return render_to_response('account.html',{ 'myapps' : myapps , 'mydetails' : mydetails }, context_instance=RequestContext(request))	
	else :
		#session does not exist for user redirect to login screen
		return render_to_response('login.html', context_instance=RequestContext(request))	

@csrf_exempt
def update_app_stats(request):
	if request.method=='POST':
		if 'apikey' in request.POST and 'secret' in request.POST :
			apikey=request.POST['apikey']
			secret=request.POST['secret']
			myapp=apps.objects.filter(apikey=apikey).filter(secret=secret)
			if len(myapp) == 0 :
				#app does not exist
				return_json_object = {
					'status' : 'appdoesnotexist',
				}
			else :
				app_id=myapp[0].id
				stat=stats(appid=app_id)
				stat.save()	
				return_json_object = {
					'status' : 'success',
				}
		else :
			return_json_object = {
				'status' : 'posterror',
			}
	else :
		return_json_object = {
			'status' : 'posterror',
		}

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)	
	


@csrf_exempt
def feedback(request):
	if request.method=='POST':
		if 'name' in request.POST and 'email' in request.POST and 'subject' in request.POST and 'message' in request.POST :
			name=request.POST['name']
			email=request.POST['email']
			subject=request.POST['subject']
			message=request.POST['message']
			tosend="Dear admin,\n You have a new socketbox feedback message .  \nFrom :  "+name+"\nEmail : "+email+"\nSubject : "+subject+"\nMessage : \n"+message
			socketbox_send_feedback_mail(tosend);
			return_json_object = {
				'status' : 'success',
			}
		else :
			return_json_object = {
				'status' : 'posterror',
			}
	else :
		return_json_object = {
			'status' : 'posterror',
		}
	
	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)	
	
@csrf_exempt
def new_password(request):
	if request.method=='POST' :
		if 'email' in request.POST and 'pass' in request.POST and 'resetcode' in request.POST:
			email=request.POST['email']
			password=request.POST['pass']
			#password=hashlib.md5(password).hexdigest()
			resetcode=request.POST['resetcode']
			user=users.objects.filter(email=email)

			if len(user) == 0 :
				return_json_object = {
				'status' : 'userdoesnotexist',
				}
			else :
				#userexists
				user_resetcode=user[0].resetcode
				if user_resetcode == resetcode :
					#reset the password
					user.update(password=password)
					return_json_object = {
						'status' : 'success',
					}
					user.update(resetcode=None)

				else :
					return_json_object = {
						'status' : 'invalidresetcode',
					}
		else :
			return_json_object = {
						'status' : 'invalidpostrequest',
					}

	else :
		return_json_object = {
			'status' : 'invalidpostrequest',
		}

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)	


@csrf_exempt
def reset_password(request):
	if request.method=='POST' :
		if 'email' in request.POST :
			email=request.POST['email']
			user=users.objects.filter(email=email)

			if len(user) == 0 :
				return_json_object = {
				'status' : 'userdoesnotexist',
				}
			else :
				#userexists
				resetcode=random_generator(10)
				link="http://socketbox.pesseacm.org/socketbox/account/reset/"+email+"/"+resetcode+"/"
				name=user[0].name
				socketbox_send_forgot_mail(email,name,link);
				user.update(resetcode=resetcode)
				return_json_object = {
				'status' : 'success',
				'resetcode' : resetcode,
				}
		else :	
				return_json_object = {
					'status' : 'noemail',
				}
	else :	
		return_json_object = {
			'status' : 'not a post',
		}

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)

@csrf_exempt
def forgot_password(request):
	return render_to_response('forgotpassword.html', context_instance=RequestContext(request))

@csrf_exempt
def reset_account(request,email,resetcode):
	if len(email) > 0 and len(resetcode) > 0 :
		return render_to_response('resetpass.html',{'email' : email , 'resetcode' : resetcode})	
	else :
		#reset URL is good
		return render_to_response('message.html',{'message' : "Invalid Reset Link , either email or resetcode is invalid!"})

@csrf_exempt
def activate_account(request,email,actcode):
	if len(email) > 0 and len(actcode) > 0 :
		user=users.objects.filter(email=email)
		if len(user) == 0: #user doesnt exist already
			return render_to_response('message.html',{'message' : "Sorry but this Email ID does not exist in our database"})
		else :
			#user exists
			user_actcode=user[0].activationcode
			#compare act codes
			if user_actcode == actcode :
				#activate the account
				user.update(activated=1)
				return render_to_response('message.html',{'message': "Congratulations your account has been activated , you may now login to your SocketBox Account"})
			else :
				return render_to_response('message.html',{'message' : "Your Email ID is valid but your activation code is invalid "})
	else :
		return render_to_response('message.html',{'message' : "Invalid Activation URL"})		

@csrf_exempt
def app_reset(request) :
	if request.method == 'POST' :
		if 'toresetappname' in request.POST :
			toresetappname=request.POST['toresetappname']
			email=request.session['email']
			password=request.session['password']
			#password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text== "success" :

				user=users.objects.filter(email=email)
				user_id=user[0].id
				myapp=apps.objects.filter(userid=user_id).filter(appname=toresetappname)
				if len(myapp) == 0 :
					#invaild appname .. thats weird :P
					return_json_object = {
						'status' : 'invalidappname',
					}
				else :
					#logic to reset app credentials	
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

					myapp.update(apikey=apikey,secret=secret)
					return_json_object = {
						'status' : 'success',
						'secret' : secret,
						'apikey' : apikey,
						'appname' : toresetappname,
					}

			else :
				return_json_object = {
						'status' : 'invalidlogin',
				}
		else :
			return_json_object = {
				'status' : 'requesterror',
			}
	else :
		return_json_object = {
			'status' : 'requesterror',
		}		
				

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)


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

def socketbox_send_activate_mail(email,name,link):
	content="Dear "+name+",\nWelcome to SocketBox .Kindly Activate your SocketBox account by clicking on the following link "+link+"\nWith Regards,\nThe SocketBox Team"
	send_mail('Activate Your SocketBox Account',content,'prashpesse@gmail.com',[email])

def socketbox_send_forgot_mail(email,name,link):
	content="Dear "+name+",\nKindly click on the following link to reset your password "+link+"\nWith Regards,\nThe SocketBox Team"
	send_mail('Reset Your SocketBox Account',content,'prashpesse@gmail.com',[email])

def socketbox_send_feedback_mail(data):
	send_mail('New Socketbox Feedback Message',data,'prashpesse@gmail.com',['prashanthjbabu@gmail.com'])

@csrf_exempt
def add_user(request):
	if request.method == 'POST' :
		if 'name' in request.POST and 'email' in request.POST and 'password' in request.POST :
			name=request.POST['name']
			email=request.POST['email']
			password=request.POST['password']
			#password=hashlib.md5(password).hexdigest()
			actcode=random_generator(10)
			link="http://socketbox.pesseacm.org/socketbox/account/activate/"+email+"/"+actcode+"/"
			user=users.objects.filter(email=email)

			if len(user) == 0: #user doesnt exist already
				new_user=users(name=name,email=email,password=password,activationcode=actcode,activated=0)
				new_user.save() # add the user
				user=users.objects.filter(email=email)
				return_json_object = {
				'status' : 'success',
				'user_id' : user[0].id,
				}
				socketbox_send_activate_mail(email,name,link);
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
		if 'navemail' in request.POST and 'navpass' in request.POST :
			email=request.POST['navemail']
			password=request.POST['navpass']
			#password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text == "userdoesnotexist" :
				return render_to_response('login.html',{'email' : email , 'message' : "User Does Not Exist!Please try again!"})
 			
 			elif return_text == "success" :
				user=users.objects.filter(email=email,activated=1)
				request.session['user_id'] = user[0].id
				request.session['email'] = user[0].email
				request.session['password'] = user[0].password				
				request.session['user_name'] = user[0].name
				return HttpResponseRedirect('/socketbox/dashboard')
 			else :
				return render_to_response('login.html',{'email' : email , 'message' : "Invalid Password!Please Try Again"})

 		else :
			return render_to_response('login.html',{'message' : "Something screwed up!Please Try Again!"})
	else :
		return render_to_response('login.html', context_instance=RequestContext(request))	
			
@csrf_exempt
def logout_user(request) :
	del request.session['user_id']
	del request.session['user_name']
	return HttpResponseRedirect('/')

def dashboard(request) :
	if 'user_id' in request.session :
		#session exists for user
		userid=request.session['user_id']
		myapps=apps.objects.filter(userid=userid)
		numberofapps=len(myapps)
		count=0
		totalmsgcount=0
		applog = []
		timelog = []
		appscount=myapps.count()
		popularappdata = {
					'status' : 'invalid',
				}
		for app in myapps :
			myappmsgcount=stats.objects.filter(appid=app.id).count()
			myapplastupdate=stats.objects.filter(appid=app.id).order_by('-time')[:1]
			apptimelog = {}
			apptimelog['time']=myapplastupdate[0].time
			timelog.append(apptimelog)
			totalmsgcount+=myappmsgcount
			appdata = {
				'name' : app.appname,
				'count' : myappmsgcount
			}
			applog.append(appdata)
			if myappmsgcount > count :
				count=myappmsgcount
				popularappdata = {
					'status' : 'valid',
					'app' : app.appname,
					'count' : myappmsgcount
				}
				

		#popularappdata = simplejson.dumps(popularappdata)

		applogs=stats.objects.filter()
		timelog=sorted(timelog,key=lambda x:x['time'],reverse=True)
		lastupdatetime=timelog[0]['time']
		print "last update time is "+str(lastupdatetime)
		return render_to_response('dashboard.html',{'lastupdatetime' : lastupdatetime , 'appscount' : appscount, 'myapps' : myapps,'applog' : applog ,'activeappstatus' : popularappdata['status'],'activeapp' : popularappdata['app'],'activeappcount' : popularappdata['count'], 'msgcount' : totalmsgcount }, context_instance=RequestContext(request))	
	else :
		#session does not exist for user redirect to login screen
		return render_to_response('login.html', context_instance=RequestContext(request))	
	
# def validate_user(email,password) :
# 	user=users.objects.filter(email=email,activated=1)
# 	if len(user) == 0 :
# 		return_json_object = {
# 			'status' : 'userdoesnotexist',
# 		}
# 	else :
# 		if user[0].password == password :
# 			return_json_object = {
# 				'status' : 'success',
# 				'userid' : user[0].id,
# 				'name' : user[0].name,
# 			}
# 		else :
# 			return_json_object = {
# 				'status' : 'incorrectpassword',
# 			}
	
# 	return_json_string = simplejson.dumps(return_json_object)
# 	return return_json_string

def validate_user_inner(email,password) :
	user=users.objects.filter(email=email,activated=1)
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

# @csrf_exempt
# def show_apps(request):
# 	if request.method == "POST" :
# 		if 'email' in request.POST and 'password' in request.POST :
# 			email=request.POST['email']
# 			password=request.POST['password']
# 			password=hashlib.md5(password).hexdigest()
# 			return_text=validate_user_inner(email,password)
# 			list_of_apps=[]
# 			if return_text== "success" :
# 				user=users.objects.filter(email=email)
# 				user_id=user[0].id
# 				myapps=apps.objects.filter(userid=user_id)
# 				return HttpResponse(serializers.serialize("json", myapps))
# 			else :
# 				return_json_object = {
# 				'status' : 'incorrectpassword',
# 				}
# 				return_json_string = simplejson.dumps(return_json_object)
# 				return HttpResponse(return_json_string)

@csrf_exempt
def show_app(request,appid) :
	myapp=apps.objects.filter(id=appid)
	if len(myapp) > 0 :
		#app exists
		user_id=myapp[0].userid

		if request.session['user_id'] == user_id :
			#correct userid
			#return HttpResponse("app id is "+appid+"app name is "+myapp[0].appname);
			myapp_json= {
			'appname' : myapp[0].appname,
			'apikey' : myapp[0].apikey,
			'secret' : myapp[0].secret,
			}

			#daylog
			daylog= []
			dateobj = datetime.datetime.now()
			delta = datetime.timedelta(days=-1)
			for i in range(30) :
				low_thresh = datetime.datetime(dateobj.year,dateobj.month,dateobj.day,00,00)
				upper_thresh = datetime.datetime(dateobj.year,dateobj.month,dateobj.day,23,59)				
				day_query = stats.objects.extra({'date' : "date(time)"}).values('date').filter(time__gt=low_thresh).filter(time__lt=upper_thresh).annotate(counter=Count('id'))
				if(len(day_query) > 0):
					day_count = day_query[0]['counter']
				else:
					day_count = 0
				data = {
					'date' : str(upper_thresh.date()),
					'count' : day_count,
				}
				daylog.append(data)
				dateobj = dateobj + delta

			#hourlog

			hourlog= []
			dateobj = datetime.datetime.now()
			delta = datetime.timedelta(hours=-1)

			for i in range(24) :
				low_thresh = datetime.datetime(dateobj.year,dateobj.month,dateobj.day,dateobj.hour,00)
				upper_thresh = datetime.datetime(dateobj.year,dateobj.month,dateobj.day,dateobj.hour,59)				
				hour_query = stats.objects.extra({'date' : "date(time)"}).values('date').filter(time__gt=low_thresh).filter(time__lt=upper_thresh).annotate(counter=Count('id'))
				if(len(hour_query) > 0):
					hour_count = hour_query[0]['counter']
				else:
					hour_count = 0
				data = {
					'time' : str(low_thresh),
					'count' : hour_count,
				}
				hourlog.append(data)
				dateobj = dateobj + delta	

			#month log	

			monthlog= []
			dateobj = datetime.now()
			#delta = datetime.timedelta(1*365/12).isoformat()
			#delta = datetime.timedelta(months=-1)
			delta= relativedelta( months = +1 )
			for i in range(12) :
				low_thresh = datetime.datetime(dateobj.year,dateobj.month,00,00,00)
				upper_thresh = datetime.datetime(dateobj.year,dateobj.month,30,23,59)
				d=datetime.datetime(dateobj.year,dateobj.month)				
				month_query = stats.objects.extra({'date' : "date(time)"}).values('date').filter(time__startswith=d).annotate(counter=Count('id'))
				if(len(month_query) > 0):
					month_count = month_query[0]['counter']
				else:
					month_count = 0
				data = {
					'time' : str(d),
					'count' : hour_count,
				}
				monthlog.append(data)
				dateobj = dateobj - delta	
	

			return render_to_response('appdetails.html',{ 'monthcounter' : monthlog , 'hourcounter' : hourlog , 'daycounter' : daylog , 'myapp' : myapp_json }, context_instance=RequestContext(request))	
		else :
			return HttpResponseRedirect('/socketbox/dashboard')	
	else :
		return HttpResponseRedirect('/socketbox/dashboard')	


@csrf_exempt
def rename_app(request):
	print "inside rename app function"
	if request.method == "POST" :
		if 'oldappname' in request.POST and 'newappname' in request.POST :
			email=request.session['email']
			password=request.session['password']
			#password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text== "success" :

				user=users.objects.filter(email=email)
				user_id=user[0].id
				old_app_name=request.POST['oldappname']
				new_app_name=request.POST['newappname']
				myapp=apps.objects.filter(userid=user_id).filter(appname=old_app_name)
				if len(myapp) == 0 :
					#invaild appname .. thats weird :P
					return_json_object = {
						'status' : 'invalidappname',
					}
				else :
					existingapp=apps.objects.filter(userid=user_id).filter(appname=new_app_name)
					if len(existingapp) == 0 :
						myapp.update(appname=new_app_name)
						return_json_object = {
							'status' : 'success',
						}
					else :
						return_json_object = {
							'status' : 'appnameexists',
						}
			else :
				return_json_object = {
						'status' : 'invalidlogin',
				}
		else :
			return_json_object = {
				'status' : 'requesterror',
			}
	else :
		return_json_object = {
			'status' : 'requesterror',
		}		
				

	return_json_string = simplejson.dumps(return_json_object)
	return HttpResponse(return_json_string)


@csrf_exempt
def delete_app(request):
	if request.method == "POST" :
		if 'todeleteappname' in request.POST :
			email=request.session['email']
			password=request.session['password']
			#password=hashlib.md5(password).hexdigest()
			return_text=validate_user_inner(email,password)
			if return_text== "success" :

				user=users.objects.filter(email=email)
				user_id=user[0].id
				app_name=request.POST['todeleteappname']

				myapp=apps.objects.filter(userid=user_id).filter(appname=app_name)
				if len(myapp) == 0 :
					#invaild appname .. thats weird :P
					return_json_object = {
						'status' : 'invalidappname',
					}
				else :
					appid=myapp[0].id
					myapp.delete()
					myappstats=stats.objects.filter(appid=appid).delete()
					return_json_object = {
						'status' : 'success',
					}
			else :
				return_json_object = {
						'status' : 'invalidlogin',
				}

			return_json_string = simplejson.dumps(return_json_object)
			return HttpResponse(return_json_string)


# @csrf_exempt
# def create_app(request):
# 	if request.method == "POST" :
# 		if 'email' in request.POST and 'password' in request.POST and 'appname' in request.POST :
# 			email=request.POST['email']
# 			password=request.POST['password']
# 			password=hashlib.md5(password).hexdigest()
# 			return_text=validate_user_inner(email,password)
# 			if return_text== "success" :

# 				user=users.objects.filter(email=email)
# 				user_id=user[0].id
# 				app_name=request.POST['appname']

# 				myapp=apps.objects.filter(userid=user_id).filter(appname=app_name)
# 				if len(myapp) == 0 :
# 					#create the app no duplicates
# 					#check if apikey is unique
# 					while True :
# 						apikey=random_generator(10)
# 						if check_unique_apikey(apikey) == 1 :
# 							break

					
# 					secret=random_generator(10)
# 					#check if secret is unique
# 					while True :
# 						secret=random_generator(10)
# 						if check_unique_secret(secret) == 1 :
# 							break
					
# 					new_app=apps(userid=user_id,appname=app_name,secret=secret,apikey=apikey)
# 					new_app.save() # add the user
# 					return_json_object = {
# 						'status' : 'appcreated',
# 						'secret' : secret,
# 						'apikey' : apikey,
# 						'appname' : app_name,
# 					}
		
# 				else :
# 					#app name already exists
# 					return_json_object = {
# 						'status' : 'appnameexists',
# 					}

# 			else :
# 				return_json_object = {
# 						'status' : 'invalidlogin',
# 				}

# 			return_json_string = simplejson.dumps(return_json_object)
# 			return HttpResponse(return_json_string)

@csrf_exempt
def create_app(request):
	if request.method == "POST" :
		if 'appname' in request.POST :
			email=request.session['email']
			password=request.session['password']
			#password=hashlib.md5(password).hexdigest()
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
						'status' : 'success',
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
	apikey="2V65STYMT7"
	secret="CQIHXCGXYR"
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