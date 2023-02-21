from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FinanceModel(models.Model):
    
    project_id = models.ForeignKey("projects.Project",on_delete=models.CASCADE,default=0)
    amt_received = models.FloatField(default=0)
    cu_percentage =models.FloatField(default=0)
    expenses = models.JSONField()
    income = models.JSONField()
    net_amt = models.FloatField(default=0)
    professor = models.JSONField()
