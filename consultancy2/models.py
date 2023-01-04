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
    password = models.CharField(max_length=100)
    campus = models.CharField(max_length = 100)
    role = models.CharField(max_length = 100)
    
    class Meta:
        db_table = "signin_users"
        
class AdminValidation(models.Model):
    
    # user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    campus = models.CharField(max_length = 100)
    role = models.CharField(max_length = 100)
    class Meta:
        db_table = "val_users"
        
    def __str__(self):
        return  f"{self.email}   |  {self.role}"


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_member = models.CharField(max_length=100,null=True)
    rolechoice = [
        ('Intern', 'Intern'),
        ('Sr Intern', 'Sr Intern'),
        ('Professor', 'Professor'),
        ('Lead Consultant', 'Lead Consultant'),
        ('Head Consultant', 'Head Consultant'),
    ]
    role = models.CharField(max_length=100,choices=rolechoice,default="Intern")
    hours = models.IntegerField()
    
    def __str__(self):
        return f"{self.team_name}"
    
    
class HourVal(models.Model):

    email = models.CharField(max_length=100)
    team = models.CharField(max_length = 100)
    hours_claimed = models.IntegerField()
    date_claimed = models.DateTimeField()
