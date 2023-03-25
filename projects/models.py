from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel,TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from consultancy2.models import *


difficulty = (
    ('1', 'Easy'),
    ('2', 'Mediocre'),
    ('3', 'Hard'),
)

status = (
    ('1', 'Working'),
    ('2', 'Stuck'),
    ('3', 'Done'),
)

category = (
    ('1', 'Extension Based'),
    ('2', 'Functional Based'),
    ('3', 'Research Based'),
    ('3', 'Government'),
)

    
# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=True)
    assign = models.ManyToManyField(User)
    
    def __str__(self):
        return f"{self.team_name}"

class Project(models.Model):
    name = models.CharField(max_length=80)
    assign = models.ManyToManyField(Team)
    category = models.CharField(max_length=15, choices=category, default=1)
    status = models.CharField(max_length=7, choices=status, default=1)
    dead_line = models.DateField()
    company = models.CharField(max_length=80)
    complete_per = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)
    documents = models.FileField(default=None,upload_to="documents/",max_length=250,null=True,blank=True)
    refdocuments = models.FileField(default=None,upload_to="documents/",max_length=250,null=True,blank=True)

    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("projects:editp", args=(self.id,))

    def __str__(self):
        return (self.name)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ManyToManyField(User)
    task_name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=250)
    difficulty = models.CharField(max_length=7, choices=difficulty, default=1)
    status = models.CharField(max_length=7, choices=status, default=1)

    class Meta:
        ordering = ['project', 'task_name']
        
    def save(self,*args,**kwargs):
        self.slug=slugify(self.task_name)
        super(Task,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("projects:viewtask", args=(self.id,))

    def __str__(self):
        return(self.task_name)
    
class ProjectComment(MPTTModel):

    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='proj_comments',blank=True,null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    username=models.CharField(max_length=250,null=True, blank=True)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['content','date_time','status']

    class MPTTMeta:
        order_insertion_by = ['date_time']

    def __str__(self):
        return self.content
    

    
