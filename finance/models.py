from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import JSONField
from jsonfield import JSONField

# Create your models here.
class ProjectFinance(models.Model):
   
    project_id = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    amt_received = models.FloatField(default=0)
    cu_percentage =models.FloatField(default=0)
    expenses = models.JSONField()
    income = models.JSONField()
    net_amt = models.FloatField(default=0)
    professor = models.JSONField()