from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
# from django.contrib.postgres.fields import JSONField
from jsonfield import JSONField

# Create your models here.
class ProjectFinance(models.Model):
   
    project_id = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
=======

# Create your models here.

class Finance(models.Model):
    
>>>>>>> 28f9b53e2ce6269cd38951cf7aac1aa71ba62bd1
    amt_received = models.FloatField(default=0)
    cu_percentage =models.FloatField(default=0)
    expenses = models.JSONField()
    income = models.JSONField()
    net_amt = models.FloatField(default=0)
<<<<<<< HEAD
    professor = models.JSONField()
=======
    professor = models.JSONField()

    
>>>>>>> 28f9b53e2ce6269cd38951cf7aac1aa71ba62bd1
