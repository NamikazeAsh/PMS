from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FinanceModel(models.Model):
    
    project_id = models.ForeignKey("projects.Project",on_delete=models.CASCADE,default=0)
    amtreceived = models.FloatField(default=0)
    cupercentage =models.FloatField(default=0)
    expenses = models.JSONField(null = True)
    incomes = models.JSONField(null = True)
    net_amt = models.FloatField(default=0)
    professor = models.JSONField(null = True)

