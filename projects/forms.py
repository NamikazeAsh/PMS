from django import forms
from django.utils.text import slugify
from .models import Task
from .models import Project
from consultancy2.models import *
from django.contrib.auth.models import User
from mptt.forms import TreeNodeChoiceField
from .models import ProjectComment
from mptt.forms import TreeNodeChoiceField
from projects.models import Team


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


class TaskRegistrationForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Professor','Sr Intern','Intern']))
    task_name = forms.CharField(max_length=80)
    difficulty = forms.ChoiceField(choices=difficulty)
    status = forms.ChoiceField(choices=status)

    class Meta:
        model = Task
        fields = ('project','assign','task_name','difficulty','status')


    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.project = self.cleaned_data['project']
        task.task_name = self.cleaned_data['task_name']
        task.difficulty = self.cleaned_data['difficulty']
        task.status = self.cleaned_data['status']
        task.save()
        assigns = self.cleaned_data['assign']
        
        for assign in assigns:
            task.assign.add((assign))

        if commit:
            task.save()

        return task


    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['placeholder'] = 'Project Name'
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['task_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['difficulty'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['class'] = 'form-control'

class ProjectRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    assign = forms.ModelMultipleChoiceField(queryset=Team.objects.all())
    category=forms.ChoiceField(choices=category)
    status = forms.ChoiceField(choices=status)
    dead_line = forms.DateField()
    company = forms.CharField(max_length=80)
    complete_per = forms.FloatField(min_value=0, max_value=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        fields = '__all__'


    def save(self, commit=True):
        Project = super(ProjectRegistrationForm, self).save(commit=False)
        Project.name = self.cleaned_data['name']
        Project.category = self.cleaned_data['category']
        Project.status = self.cleaned_data['status']
        Project.dead_line = self.cleaned_data['dead_line']
        Project.company = self.cleaned_data['company']
        Project.complete_per = self.cleaned_data['complete_per']
        Project.description = self.cleaned_data['description']
        Project.slug = slugify(str(self.cleaned_data['name']))
        Project.save()
        assigns = self.cleaned_data['assign']
        for assign in assigns:
            Project.assign.add((assign))

        if commit:
            Project.save()

        return Project


    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Project Name'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['placeholder'] = 'Category'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Status'
        self.fields['dead_line'].widget.attrs['class'] = 'form-control'
        self.fields['dead_line'].widget.attrs['placeholder'] = 'mm/dd/yyyy'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['placeholder'] = 'Company'
        self.fields['complete_per'].widget.attrs['class'] = 'form-control'
        self.fields['complete_per'].widget.attrs['placeholder'] = 'Complete %'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Type here the project description...'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        
        
class ProjectCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=ProjectComment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = ProjectComment
        fields = ('parent','content')

        widgets = {
            'content': forms.Textarea(attrs={'class': 'ml-3 mb-3 form-control border-0 comment-add rounded-0', 'rows': '1', 'placeholder': 'Add a comment'}),
        }

    def save(self, *args, **kwargs):
        ProjectComment.objects.rebuild()
        return super(ProjectCommentForm, self).save(*args, **kwargs)
    
class TeamRegistrationForm(forms.ModelForm):
    team_name = forms.CharField(max_length=100)
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Professor','Sr Intern','Intern']))
    class Meta:
        model = Team
        fields = '__all__'
        
    def save(self, commit=True):
        team=super(TeamRegistrationForm, self).save(commit=False)
        team.team_name = self.cleaned_data['team_name']
        team.save()
        assigns = self.cleaned_data['assign']
        for assign in assigns:
            team.assign.add((assign))

        if commit:
            team.save()

        return team
    
    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['team_name'].widget.attrs['class'] = 'form-control'
        self.fields['team_name'].widget.attrs['placeholder'] = 'Team Name'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        
        
class FileForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["documents"]
        
        
        