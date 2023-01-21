from django.db import models

# Create your models here.
class UserScore(models.Model):
    email = models.CharField(max_length=100)
    score = models.IntegerField()
    
class UserIndex(models.Model):
    email = models.CharField(max_length=100)
    index =  models.FloatField()