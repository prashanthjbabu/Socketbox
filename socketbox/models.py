from django.db import models
import datetime
# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    activationcode = models.CharField(max_length=10)
    resetcode = models.CharField(max_length=10,null=True)
    activated = models.IntegerField(max_length=1)
    accountcreation = models.DateTimeField(auto_now_add = True,default=datetime.datetime.now)
    lastlogin = models.DateTimeField(auto_now_add = True,default=datetime.datetime.now)
    def __unicode__(self):
        return "%s %s %s %d" % (self.name, self.email, self.password ,self.activated)

class apps(models.Model):
    userid = models.IntegerField(max_length=10)
    appname = models.CharField(max_length=50)
    apikey = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    def __unicode__(self):
        return "%s %s %s %s" % (self.userid, self.appname, self.apikey,self.secret)

class stats(models.Model):
    appid = models.IntegerField(max_length=10)
    time = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return "%s %s" % (self.appid, self.time)
    