from distutils.command.upload import upload
from email.policy import default
from enum import unique
from pickle import TRUE
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser

from django.contrib.auth.models import User


class SignInInsert(models.Model):
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100,default="-")
    firstname = models.CharField(max_length=100,default="-")
    lastname = models.CharField(max_length=100,default="-")
    password = models.CharField(max_length=100)
    campus = models.CharField(max_length = 100)
    role = models.CharField(max_length = 100)
    
    class Meta:
        db_table = "signin_users"
        

class AdminValidation(models.Model):
    
    # user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100,default="-")
    firstname = models.CharField(max_length=100,default="-")
    lastname = models.CharField(max_length=100,default="-")
    password = models.CharField(max_length=100)
    campus = models.CharField(max_length = 100)
    role = models.CharField(max_length = 100)
    hours = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='images/profile_pics/', blank=True)
    
    class Meta:
        db_table = "val_users"


class HourVal(models.Model):

    email = models.CharField(max_length=100)
    hours_claimed = models.IntegerField()
    description = models.CharField(max_length=100,default="-")


class RequestModel(models.Model):

    name = models.CharField(max_length=100)
    requestmsg = models.CharField(max_length=1000)


