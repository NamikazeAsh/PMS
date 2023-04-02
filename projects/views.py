from django.shortcuts import render,get_object_or_404, HttpResponseRedirect, redirect,HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from register.models import Project
from projects.models import Task,Team,ProjectComment
from projects.forms import ProjectCommentForm
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm
from projects.forms import TeamRegistrationForm
from consultancy2.decorators import *
from finance.models import FinanceModel
from consultancy2.decorators import allowed_users

from django.urls import reverse
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail

import pandas as pd

import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.files import File
from .forms import FileForm

from tkinter.filedialog import *


def findtemp(request):
    if request.user.groups.filter(name='Intern').exists():
        return 'intern/tempintern.html'
    elif request.user.groups.filter(name='Sr Intern').exists():
        return 'srintern/tempsrintern.html'
    elif request.user.groups.filter(name='Professor').exists():
        return 'srintern/tempsrintern.html'
    elif request.user.groups.filter(name='Lead Consultant').exists():
        return 'consultant/templeadc.html'
    elif request.user.groups.filter(name='Head Consultant').exists():
        return 'consultant/tempheadc.html'
    
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
        members = []
        for tassid in tass:
            members.append(User.objects.get(id = tassid[0]).username) 
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
    
@login_required(login_url='login')
def edit_task(request,id):
    task = Task.objects.get(id=id)
    current_user = request.user
    form=TaskRegistrationForm(instance=task)
    if request.method == 'POST':
        
        form = TaskRegistrationForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('projects:task',id= current_user.id)
    var = findtemp(request)
    
    context = {'form':form,'temp':var,}
    return render(request, 'projects/edit_task.html', context)  

def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        var = findtemp(request)
        context = {'form': form,'temp':var,}
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


        
def taskprofile1(request):
    tasks = Task.objects.filter()
    context = {
        'tasks': tasks,
    }
    return render(request,'projects/alltasks.html',context)

def deltask(request,task):

    task = get_object_or_404(Task,id=task)
    task.assign.remove(request.user.id)
    if task.assign.exists() == False:
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
    
    # ---------------------------- Completion handler ---------------------------- #
    projc = Project.objects.all()
    for project in projc:
        if project.documents:
            project.status = 3
            if project.status == 3:
                project.complete_per=100
            project.save()
    # ----------------------------------- xxxx ----------------------------------- #
    
    projects = Project.objects.all()
    projteamassoc = []
    for a in projects:
        for idi in Project.objects.values_list('assign').filter(id = a.pk):
            if idi[0] != None:    
                if Team.objects.get(id = idi[0]).team_name:    
                    teamname = Team.objects.get(id = idi[0]).team_name
                    projteamassoc.append([a.name,idi[0],teamname])
            else:
                projteamassoc.append([a.name,"-","-"])
    
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
def edit_project(request,id):
    project = Project.objects.get(id=id)
    form=ProjectRegistrationForm(instance=project)
    if request.method == 'POST':
        
        form = ProjectRegistrationForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:projects')
    var = findtemp(request)
    
    context = {'form':form,'temp':var,}
    return render(request, 'projects/edit_project.html', context)    

@login_required(login_url='login')
@allowed_users(allowed_roles=['Head Consultant'])
def ProjectProfile(request, id):
    projdet = Project.objects.filter(id = id)
    
    var = findtemp(request)
    pcomments = get_object_or_404(Project, id=id)
    username = request.user.is_authenticated
    allcomments = pcomments.proj_comments.filter(status=True)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 4)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None
    
    projteam = Project.objects.values_list('assign').filter(id=id)
    team_id = []
    team_name = []
    team_members_id = []
    team_members = []
    
    for tm in projteam:    
        team_id.append(tm[0])
    for tid in team_id:
        print("TID: ",tid)
        if tid != None:
            team_name.append(Team.objects.get(id = tid))
        else:
            team_name.append("-")
        
    projteam_mem = Team.objects.filter(id = tid).values_list('assign')
    for tm2 in projteam_mem:
        team_members_id.append(tm2[0])
    for tid2 in team_members_id:
        team_members.append(User.objects.get(id = tid2))
    
    pcname = str(Project.objects.get(id=id).company)
    
    if request.method == 'POST':
        comment_form = ProjectCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.username=request.user.username
            user_comment.project = pcomments
            user_comment.save()
            print('User saved')
            return redirect('projects:project-profile',id= pcomments.id)
        
    else:
        comment_form = ProjectCommentForm()

    finance_details = FinanceModel.objects.filter(project_id = id)
    incomeDetails = []
    expenseDetails = []
    profDetails = []
    profNames = ""
    profRatio = ""
    basicDetails = {}
    totalIncome = 0
    totalExpense = 0
    cuShare = 0
    netAmount = 0 

    if finance_details:
        basicDetails = finance_details[0]
        cuShare = ((basicDetails.cupercentage)*(basicDetails.amtreceived))/100
        if finance_details[0].incomes:
            incomeDetails = json.loads(finance_details[0].incomes)['add']
            incomeDetails = list(map(returnJson, incomeDetails))

            for i in incomeDetails:
                totalIncome = totalIncome + (int(i['amount']))

        if finance_details[0].expenses:
            expenseDetails = json.loads(finance_details[0].expenses)['less']
            expenseDetails = list(map(returnJson, expenseDetails))

            for i in expenseDetails:
                totalExpense = totalExpense + (int(i['amount']))

        if finance_details[0].professor:
            profDetails = json.loads(finance_details[0].professor)['professors']
            profDetails = list(map(returnJson, profDetails))        
                
        netAmount = ((basicDetails.amtreceived)-(cuShare)-(totalExpense) 
        + (totalIncome))

        for i in profDetails:
            i['ratioAmount'] = (int(i['ratio']) * netAmount)/10
    
        for i in profDetails:
            profNames = profNames + i['Professor'] + ", "
            profRatio = profRatio + i['ratio'] + ":"

    return render(request, 'projectprofile.html', {'projdet': projdet,
        'pid':id,
        'temp':var,
        'team_name':team_name,
        'team_members':team_members,
        'pcname':pcname,
        'pcomments': pcomments,
        'comments':  user_comment,
        'comments': comments,
        'comment_form': comment_form, 
        'allcomments': allcomments,
        'financeDetails': basicDetails,
        'cuShare': cuShare,
        'totalIncome': totalIncome,
        'totalExpense': totalExpense,
        'netAmount': netAmount,
        'profDetails': profDetails,
        'profNames': profNames,
        'profRatio': profRatio,
        'incomeDetails': incomeDetails,
        'expenseDetails': expenseDetails,
        'username':username,})

def returnJson(obj):
    return json.loads(obj)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Lead Consultant','Head Consultant'])
def deletecomment(request,id):
    users_comment = get_object_or_404(ProjectComment, id=id)
    
    users_comment.delete()
    # return redirect('projects:project-profile',id=users_comment.id)
    pid = users_comment.project.id
    # return ProjectProfile(request,pid)
    return redirect('projects:project-profile',pid)

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


import os
import mimetypes

@login_required(login_url='login')
def DownloadAllProjectReport(request):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dfd = Project.objects.all().values()
    df = pd.DataFrame(dfd)
    csvtitle = request.user.username
    df.to_csv("Reports/Project/" + csvtitle + ".csv",index=False)
    
    filename = csvtitle + '.csv'
    filepath =  BASE_DIR + '/Reports/Project/' + filename
    path = open(filepath,'r')
    mime_type = mimetypes.guess_type(filepath)
    response = HttpResponse(path,content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    
    return response

@login_required(login_url='login')
def UploadProjectDocs(request,id):
    
    fuo = Project.objects.get(id=id)
    
    if request.method == 'POST':
        if request.FILES:
            fuo.documents = request.FILES['upload']
            fuo.save()
        else:
            print("Nothing to upload")
    
    return projects(request)

@login_required(login_url='login')
def UploadRefProjectDocs(request,id):
    
    fuo = Project.objects.get(id=id)
    
    if request.method == 'POST':
        if request.FILES:
            fuo.refdocuments = request.FILES['refupload']
            fuo.save()
        else:
            print("Nothing to upload")
    
    return projects(request)

def editTeamInfo(request, teamname):
    # Edit Team Code Here
    pass

#     return redirect('/projects/team-views/')

def deleteTeamInfo(request, teamname):
    # Delete Team Code Here
    # teamname is the id of the table
    # remove key pair from table where key is teamname
    # return redirect('/projects/team-views/')
    pass

# @login_required(login_url='login')
# def editTeamInfo(request, teamname):
#     if request.method == 'POST':
#         form = TeamRegistrationForm(request.POST)
#         context = {'form': form}
#         if form.is_valid():
#             form.save()
#             created = True
#             form = TeamRegistrationForm()
#             var = findtemp(request)
#             context = {
#                 'created': created,
#                 'form': form,
#                 'temp':var,
#             }
#             return render(request, 'projects/editTeam.html', context)
#         else:
#             return render(request, 'projects/editTeam.html', context)
#     else:
#         form = TeamRegistrationForm()
#         var = findtemp(request)
#         context = {
#             'form': form,
#             'temp':var,
#         }
#         return render(request,'projects/editTeam.html', context)

def deleteExpenseInfo(request, id, eid):
    # Expense Information Delete Code Here
    financeExpense = FinanceModel.objects.get(project_id = id)
    existingexpenses = json.loads(financeExpense.expenses)['less']
    for i in range(len(existingexpenses)):
        updateExpense = json.loads(existingexpenses[i])
        if updateExpense['id'] == eid:
                del existingexpenses[i]
                break
    
    updatedExpenseDict = {'less': existingexpenses}
    financeExpense.expenses = json.dumps(updatedExpenseDict)
    financeExpense.save()

        
    return redirect(f'/projects/projects/project/{id}')

def deleteIncomeInfo(request, id, iid):
    # Income Information Edit Code Here
    financeIncome = FinanceModel.objects.get(project_id = id)
    existingincome = json.loads(financeIncome.incomes)['add']
    for i in range(len(existingincome)):
        updateIncome = json.loads(existingincome[i])
        if updateIncome['id'] == iid:
                del existingincome[i]
                break
    
    updatedIncomeDict = {'add': existingincome}
    financeIncome.incomes = json.dumps(updatedIncomeDict)
    financeIncome.save()
    return redirect(f'/projects/projects/project/{id}')

def deleteProfessorInfo(request, id, pid):
    # Professor Information Edit Code Here
    financeProf = FinanceModel.objects.get(project_id = id)
    existingprof = json.loads(financeProf.professor)['professors']
    for i in range(len(existingprof)):
        updateProf = json.loads(existingprof[i])
        if updateProf['id'] == pid:
                del existingprof[i]
                break
    
    updatedProfDict = {'professors': existingprof}
    financeProf.professor = json.dumps(updatedProfDict)
    financeProf.save()
    return redirect(f'/projects/projects/project/{id}')