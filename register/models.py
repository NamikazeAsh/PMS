from django.db import models
from django.contrib.auth.models import User
from projects.models import Project,Task
from mptt.models import MPTTModel,TreeForeignKey


class UserProfile(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.user))



