from django.db import models

# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    activationcode = models.CharField(max_length=10)
    resetcode = models.CharField(max_length=10)
    activated = models.IntegerField(max_length=1)
    def __unicode__(self):
        return "%s %s %s %d" % (self.name, self.email, self.password ,self.activated)

class apps(models.Model):
    userid = models.IntegerField(max_length=10)
    appname = models.CharField(max_length=50)
    apikey = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    def __unicode__(self):
        return "%s %s %s %s" % (self.userid, self.appname, self.apikey,self.secret)
