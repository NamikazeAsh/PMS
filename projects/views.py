from django.shortcuts import render,get_object_or_404, HttpResponseRedirect, redirect,HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from register.models import Project
from projects.models import Task,Team
from projects.forms import NewCommentForm
from projects.forms import ProjectCommentForm
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm
from projects.forms import TeamRegistrationForm

from django.urls import reverse
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail

import pandas as pd

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.files import File
from .forms import FileForm


def findtemp(request):
    if request.user.groups.filter(name='Intern').exists():
        return 'intern/tempintern.html'
    elif request.user.groups.filter(name='Sr Intern').exists():
        return 'srintern/tempsrintern.html'
    elif request.user.groups.filter(name='Professor').exists():
        return 'srintern/tempsrintern.html'
    elif request.user.groups.filter(name='Lead Consultant').exists():
        return 'consultant/tempprof.html'
    elif request.user.groups.filter(name='Head Consultant').exists():
        return 'consultant/tempprof.html'
# Create your views here.
def teams(request):
    
    teams = Team.objects.all()
    teamd = {}
    tl = teams.values_list()

    team_name = []
    for tname in tl:
        team_name.append(tname[1])
        
    team_members = []
    for tname2 in team_name:
        tass = Team.objects.filter(team_name = tname2).values_list('assign')
        members = ""
        for tassid in tass:
            members+= User.objects.get(id = tassid[0]).username + " | "
        team_members.append(members)
    
    for i in range(len(team_name)):
        teamd[team_name[i]] = team_members[i]
    
    var = findtemp(request)
    context = {
        'temp':var,
        'teamd':teamd,
    }
    return render(request, 'projects/teamviews.html', context)

def taskprofile(request,id):
    tasks = Task.objects.filter(assign = id)
    var = findtemp(request)
    context = {
        'tasks': tasks,
        'temp':var,
    }
    return render(request,'projects/tasks.html',context)



def projectprofile(request,id):
    proj = Project.objects.filter(assign = id)
    var = findtemp(request)
    context = {
        'proj': proj,
        'temp':var,
    }
    return render(request,'projects/allprojects.html',context)


def newTask(request):
    var = findtemp(request)
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form,
        'temp':var,}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
                'temp':var,
            }
            
            
            # ------------------------------- Email Section ------------------------------ #
            # send_mail(
            #     '[Christ Consulting] Task assigned!',
            #     'Task has been assigned',
            #     'noreply.christconsulting@gmail.com',
            #     ['ashwin.satish@science.christuniversity.in'],
            #     fail_silently=False,
            # )
            # print("Email Sent")
            
            return render(request, 'projects/new_task.html', context)
        else:
            return render(request, 'projects/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
            'temp': var,
        }
        return render(request,'projects/new_task.html', context)

def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            var = findtemp(request)
            context = {
                'created': created,
                'form': form,
                'temp':var,
            }
            return render(request, 'projects/new_project.html', context)
        else:
            return render(request, 'projects/new_project.html', context)
    else:
        form = ProjectRegistrationForm()
        var = findtemp(request)
        context = {
            'form': form,
            'temp':var,
        }
        return render(request,'projects/new_project.html', context)

class edittask(generic.UpdateView):
    model = Task
    fields = ["status"]
    template_name = "projects/etask.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        var = findtemp(self.request)
        context["temp"] = var
        
        return context
        

class editproject(generic.UpdateView):
    model = Project
    fields = ["status","assign","efforts","dead_line"]
    template_name = "projects/eproject.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        var = findtemp(self.request)
        context["temp"] = var
        
        return context
        
def taskprofile1(request):
    tasks = Task.objects.filter()
    context = {
        'tasks': tasks,
    }
    return render(request,'projects/alltasks.html',context)

def comment(request):
    return render(request,'projects/vtask.html')
    


def viewtask(request, task):

    var = findtemp(request)
    task = get_object_or_404(Task, id=task)

    allcomments = task.comments.filter(status=True)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.username=request.user.username
            user_comment.task = task
            user_comment.save()
            # return HttpResponseRedirect('/' +'projects/etask'+'/'+task.slug)
            return redirect('projects:viewtask',task= task.id)
        
    else:
        comment_form = NewCommentForm()
    return render(request, 'projects/vtask.html', {'task': task, 'comments':  user_comment, 'comments': comments, 'comment_form': comment_form, 'allcomments': allcomments, 'temp':var,})

def deltask(request,task):
    
    task = get_object_or_404(Task,id=task)
    task.delete()
    
    tasks = Task.objects.filter(assign = request.user.id)
    var = findtemp(request)
    context = {
        'tasks': tasks,
        'temp':var,
    }
    return render(request,'projects/tasks.html',context)

@login_required(login_url='login')
def projects(request):
    
    projects = Project.objects.all()
    projteamassoc = []
    for a in projects:
        for idi in Project.objects.values_list('assign').filter(id = a.pk):
            teamname = Team.objects.get(id = idi[0]).team_name
            projteamassoc.append([a.name,idi[0],teamname])
    
    teams = Team.objects.all()
    avg_projects = Project.objects.all().aggregate(Avg('complete_per'))['complete_per__avg']
    tasks = Task.objects.all()
    overdue_tasks = tasks.filter(status='2')
    var = findtemp(request)
    
    form = FileForm(request.POST or None,request.FILES or None)
    
    context = {
        'avg_projects' : avg_projects,
        'projects' : projects,
        'projteamassoc':projteamassoc,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
        'temp':var,
        'teams':teams,
        'form':form,
    }
    return render(request, 'projects/projects.html', context)

@login_required(login_url='login')
def ProjectProfile(request,id):
    
    projdet = Project.objects.filter(id = id)
    var = findtemp(request)
    pcomments = get_object_or_404(Project, id=id)
    
    allcomments = pcomments.proj_comments.filter(status=True)
    print('n-',allcomments)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None
    
    projteam = Project.objects.values_list('assign').filter(id=id)
    print(projteam)
    team_id = []
    team_name = []
    team_members_id = []
    team_members = []
    
    for tm in projteam:    
        team_id.append(tm[0])
    for tid in team_id:
        team_name.append(Team.objects.get(id = tid))
    
    projteam_mem = Team.objects.filter(id = tid).values_list('assign')
    print(projteam_mem)
    for tm2 in projteam_mem:
        team_members_id.append(tm2[0])
    for tid2 in team_members_id:
        team_members.append(User.objects.get(id = tid2))
    
    pcname = str(Project.objects.get(id=id).company)
<<<<<<< HEAD
    print(pcname)    
    
    if request.method == 'POST':
        comment_form = ProjectCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.username=request.user.username
            user_comment.pcomments = pcomments
            user_comment.save()
            print('saved')
            return redirect('projects:project-profile',id= pcomments.id)
        
    else:
        comment_form = ProjectCommentForm()
    return render(request, 'projectprofile.html', {'projdet': projdet,
=======
    
    var = findtemp(request)
    context = {
        'projdet': projdet,
>>>>>>> 28f9b53e2ce6269cd38951cf7aac1aa71ba62bd1
        'pid':id,
        'temp':var,
        'team_name':team_name,
        'team_members':team_members,
        'pcname':pcname,
        'pcomments': pcomments,
        'comments':  user_comment,
        'comments': comments,
        'comment_form': comment_form, 
        'allcomments': allcomments,})

@login_required(login_url='login')
def newTeam(request):
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = TeamRegistrationForm()
            var = findtemp(request)
            context = {
                'created': created,
                'form': form,
                'temp':var,
            }
            return render(request, 'projects/new_team.html', context)
        else:
            return render(request, 'projects/new_team.html', context)
    else:
        form = TeamRegistrationForm()
        var = findtemp(request)
        context = {
            'form': form,
            'temp':var,
        }
        return render(request,'projects/new_team.html', context)

@login_required(login_url='login')
def DownloadProjectReport(request,id):
    
    dfd = Project.objects.filter(id = id).values()
    df = pd.DataFrame(dfd)
    csvtitle = Project.objects.filter(id=id).values('name')
    for title in csvtitle:
        df.to_csv("Reports/Project/" + title["name"] + ".csv")
    
    return projects(request)

@login_required(login_url='login')
def DownloadAllProjectReport(request):

    dfd = Project.objects.all().values()
    df = pd.DataFrame(dfd)
    csvtitle = request.user.first_name
    df.to_csv("Reports/Project/" + csvtitle + ".csv")
    
    return projects(request)

@login_required(login_url='login')
def UploadProjectDocs(request,id):
    
    fuo = Project.objects.get(id=id)
    
    if request.method == 'POST':
        fuo.documents = request.FILES['upload']
        fuo.save()
        print("saved")
    
    # documents = fuo.documents
    # form = FileForm(instance=fuo)
    # if form.is_valid():
    #     form.save()
    # context={
    #     'form':form,
    #     'documents':documents
    # }
    
    return projects(request)
