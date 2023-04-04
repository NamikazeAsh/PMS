from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
# Create your views here.
from multiprocessing import context
from projects.models import Project,Team
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm

from consultancy2 import models
from register.forms import RegistrationForm
from .models import AdminValidation, SignInInsert,HourVal,RequestModel
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from register.models import UserProfile
from finance.models import *
from projects import views
from projects.models import ProjectComment
from projects.models import Task

import datetime
import json

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


from .decorators import unauthorized_users,allowed_users
flag = True


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


@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')


def SignIn(request): 
    
    if request.user.is_authenticated:
        
        if request.user.groups.filter(name='Intern').exists():
            
            uid = request.user.id
            teams = Team.objects.filter(assign = uid).values_list()
            teamslist = []
            for t in teams:
                teamslist.append(t[0])

            refprojectslist = []
            for tid in teamslist:
                project = Project.objects.filter(assign = tid)
                if project.exists(): 
                    if project[0].refdocuments:
                        refprojectslist.append(project[0])
            
            return render(request,'intern/tempintern.html',{"refprojectslist":refprojectslist})
        
        elif request.user.groups.filter(name='Sr Intern').exists():
            
            uid = request.user.id
            teams = Team.objects.filter(assign = uid).values_list()
            teamslist = []
            for t in teams:
                teamslist.append(t[0])

            refprojectslist = []
            for tid in teamslist:
                project = Project.objects.filter(assign = tid)
                if project.exists():    
                    if project[0].refdocuments:
                        refprojectslist.append(project[0])
            
            return render(request,'srintern/tempsrintern.html',{"refprojectslist":refprojectslist})
        
        elif request.user.groups.filter(name='Professor').exists():
            
            uid = request.user.id
            teams = Team.objects.filter(assign = uid).values_list()
            teamslist = []
            for t in teams:
                teamslist.append(t[0])

            refprojectslist = []
            for tid in teamslist:
                project = Project.objects.filter(assign = tid)
                if project.exists():    
                    if project[0].refdocuments:
                        refprojectslist.append(project[0])
                        
            return render(request,'srintern/tempsrintern.html',{"refprojectslist":refprojectslist})
        
        elif request.user.groups.filter(name='Lead Consultant').exists():
            return render(request,'consultant/templeadc.html')
        
        elif request.user.groups.filter(name='Head Consultant').exists():

            finanaceData = FinanceModel.objects.all()

            # Making Bar Graph for Highest total Income
            net_amount = []
            tempDict = dict()

            for project in finanaceData:
                projectName = Project.objects.filter(id=project.project_id_id)[0].name
                tempDict[projectName] = project.net_amt
            tempDict = sorted(tempDict.items(), key=lambda x:x[1], reverse=True)
            tempDict = dict(tempDict[:10])
            random_x = list(tempDict.keys())
            random_y = list(tempDict.values())
            fig = px.bar(x = random_x, y = random_y, title = "Projects with Top Total Amount", labels={"x": "Project name","y": "Total Amount"},) 
            bar_plot = plot(fig, output_type="div")
            context = {'plot_div_main': bar_plot}

            # Making Waterfall Graph for Every Project
            projectNameWaterfall = []
            initialAmount = []
            amountToCU = []
            expenses = [-5000,-500,-68200,0]
            incomes = [6000,1000,69000,0]
            totalAmount = []

            for project in finanaceData:
                projectNameWaterfall.append(Project.objects.filter(id=project.project_id_id)[0].name)
                initialAmount.append(project.amtreceived)
                amountToCU.append(-abs(project.amtreceived * (project.cupercentage/100)))
                # expenses.append(0 if finanaceData[3].expenses == None else -abs(project.net_expenses))
                # expenses.append(project.net_expenses)
                # incomes.append(0 if finanaceData[3].expenses == None else project.net_incomes)
                # incomes.append(project.net_incomes)
                totalAmount.append(project.net_amt)

            for i in range(len(projectNameWaterfall)):
                fig = go.Figure(go.Waterfall(
                    measure = ["relative", "relative", "relative", "relative", "total"],
                    x = ["Recieved Amount", "Amount to CU", "Expenses", "Incomes", "Total"],
                    textposition = "outside",
                    text = [f"{initialAmount[i]}", f"{amountToCU[i]}", f"{expenses[i]}", f"{incomes[i]}", f"{totalAmount[i]}"],
                    y = [initialAmount[i], amountToCU[i], expenses[i], incomes[i], totalAmount[i]],
                    connector = {"line":{"color":"rgb(63, 63, 63)"}},
                ))
                fig.update_layout(
                    title = projectNameWaterfall[i],
                    showlegend = False,
                    width = 500, height =  550, 
                )
                waterfall_plot = plot(fig, output_type="div")
                context[f"{projectNameWaterfall[i]}"] = waterfall_plot

            # print(context["Project1"])
            context["projectNames"] = projectNameWaterfall
            return render(request, 'consultant/tempheadc.html', context)
        
        else:
            return AdminDashboard(request)
    else:    
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            context = {'form':form}
            if form.is_valid():
                
                saverecord = SignInInsert()
                saverecord.email = form.cleaned_data.get("email")
                saverecord.username = form.cleaned_data.get("username")
                saverecord.firstname = form.cleaned_data.get("first_name")
                saverecord.lastname = form.cleaned_data.get("last_name")
                saverecord.password = form.cleaned_data.get("password1")
                saverecord.campus = request.POST.get('campus')
                saverecord.role = request.POST.get('role')
                saverecord.save()
                
                created = True
                context = {'created' : created}
                return render(request, 'signup.html', context)
            else:
                return render(request, 'signup.html', context)
                
                
        else:
            form = RegistrationForm()
            var = findtemp(request)        
            context = {
                'form' : form,
                'temp' : var,
            }
            
            return render(request,'signup.html',context)


def LogIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        av = SignInInsert.objects.values('username','password')
        
        avc = {}
        avc['username'] = request.POST['username']
        avc['password'] = request.POST['password']
        
        
        if avc not in av:
            if form.is_valid():
                
                    authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
                    login(request, authenticated_user)
                    if request.user.groups.filter(name='Intern').exists():
                        return render(request,'intern/tempintern.html')
                    elif request.user.groups.filter(name='Sr Intern').exists():
                        return render(request,'srintern/tempsrintern.html')
                    elif request.user.groups.filter(name='Professor').exists():
                        return render(request,'srintern/tempsrintern.html')
                    elif request.user.groups.filter(name='Lead Consultant').exists():
                        return render(request,'consultant/templeadc.html')
                    elif request.user.groups.filter(name='Head Consultant').exists():
                        labels = ["Recieved Amount", "Amount to CU", "Expenses", "Incomes", "Total"]
                        data = [5000, 500, 500, 4000, 8000]
                        context = {'labels': labels, 'data': data}
                        return render(request,'consultant/tempheadc.html', context)
                        # return render(request,'consultant/tempheadc.html')

                    elif request.user.groups.filter(name='Admin').exists():
                        return redirect('admindashboard')
                    

            else:
                var = findtemp(request)
                return render(request, 'login.html', {'login_form':form,'temp':var,})
        else:
            adminvalerrormsg = True
            var = findtemp(request)
            return render(request, 'login.html', {'login_form':form,'temp':var,'adminvalerrormsg':adminvalerrormsg})
        
    else:
        form = AuthenticationForm()
        
    var = findtemp(request)
    return render(request, 'login.html', {'login_form':form,'temp':var,})


def LogOut(request):
    logout(request)
    return redirect('login')


@login_required(login_url='admin')
@allowed_users(allowed_roles=['Admin'])
def AdminVal(request):

    details = SignInInsert.objects.all()
    return render(request,"adminval.html",{'detail':details})


@login_required(login_url='admin')
@allowed_users(allowed_roles=['Admin'])
def AdminValAcc(request,id):

    auser = SignInInsert.objects.get(id=id)
    saverecord = AdminValidation()
    saverecord.email = auser.email
    saverecord.username = auser.username
    saverecord.firstname = auser.firstname
    saverecord.lastname = auser.lastname
    saverecord.password = auser.password
    saverecord.campus = auser.campus
    saverecord.role = auser.role
    saverecord.save()
    
    user = User.objects.create_user(auser.username,auser.email,auser.password)
    user.save()
    
    up = UserProfile.objects.create(user=user)
    up.save()
    
    group = Group.objects.get(name=auser.role)
    user.groups.add(group)
    
    auser.delete()
    
    return HttpResponseRedirect(reverse('adminval'))


@login_required(login_url='admin')
@allowed_users(allowed_roles=['Admin'])
def AdminValDel(request,id):

    duser = SignInInsert.objects.get(id=id)
    duser.delete() 
    details = SignInInsert.objects.all()
    return HttpResponseRedirect(reverse('adminval'))


@login_required(login_url='login')
def TempIntern(request):
    return render(request,'intern/tempintern.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern'])
def TempSrIntern(request):
    return render(request,'srintern/tempsrintern.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern','Intern','Professor','Lead Consultant','Head Consultant'])
def UsersProfile(request):
    return render(request,"profile.html",context)

@login_required(login_url='login')
def ProjectProfile(request,id):
    
    return render(request,"projectprofile.html",context,id)

@login_required(login_url='login')
def UserHourTracking(request):
    if request.user.groups.filter(name='Intern').exists():
        return redirect('user-hours-i')
    elif request.user.groups.filter(name='Sr Intern').exists():
        return redirect('user-hours-p')
    elif request.user.groups.filter(name='Professor').exists():
        return redirect('user-hours-p')
    elif request.user.groups.filter(name='Head Consultant').exists():
        return redirect('user-hours-p')
    elif request.user.groups.filter(name='Lead Consultant').exists():
        return redirect('user-hours-p')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Intern'])
def UserHourTrackingIntern(request):
    
    if request.method == "POST":

        saverecord = HourVal()
        saverecord.email = request.user.email
        saverecord.hours_claimed = request.POST.get('hours')
        saverecord.date_claimed = datetime.datetime.now()
        saverecord.team = request.POST.get('team')
        saverecord.description = request.POST.get('description')
        saverecord.save()
        
        return redirect('user-hours-i')
        
    var = findtemp(request)
    
    freehouro = AdminValidation.objects.get(email = request.user.email)
    
    context = {
        "temp": var,
        "freehourso":freehouro,
    }
    
    return render(request,"userhour_intern.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern','Professor','Head Consultant','Lead Consultant'])
def UserHourTrackingProfessor(request):
    users = UserProfile.objects.all()
    if request.method == "POST":
        
        uhour = request.POST.get('hours')
        
        valusers = AdminValidation.objects.get(email = request.user.email)
        updhour = valusers.hours
        newhour = updhour + int(uhour)
        
        valusers.hours = newhour
        valusers.save()
        
        return redirect('user-hours-p') #home/signup autodirect home
        
    details = HourVal.objects.all()
    freehouro = AdminValidation.objects.get(email = request.user.email)
    
    var = findtemp(request)
    context = {
        "temp": var,
        "details":details,
        "freehourso":freehouro,
        'users': users,
    }
    
    return render(request,"userhour_professor.html",context)

@login_required(login_url='login')
def UserHourTrackingAccept(request,id):

    hv = HourVal.objects.get(id=id)

    ave = hv.email
    av = AdminValidation.objects.get(email = ave)

    vhour = hv.hours_claimed
    av.hours = vhour + av.hours
    av.save()
    hv.delete() 
    
    return HttpResponseRedirect(reverse('user-hours-p'))

@login_required(login_url='login')
def UserHourTrackingDeny(request,id):
    
    delentry = HourVal.objects.get(id=id)
    delentry.delete()
    return HttpResponseRedirect(reverse('user-hours-p'))


@login_required(login_url='admin:login')
@allowed_users(allowed_roles=['Admin'])
def AdminDashboard(request):
    users = User.objects.all()
    vusers = AdminValidation.objects.all()
    teams = Team.objects.all()
    projects = Project.objects.all()
    
    context = {
        'users':users,
        'vusers':vusers,
        'teams':teams,
        'projects':projects
    }
    return render(request,"admindashboard.html",context=context)


def context(request): # send context to base.html
    # if not request.session.session_key:
    #     request.session.create()
    users = User.objects.all()
    users_prof = UserProfile.objects.all()
    if request.user.is_authenticated:
        try:
            users_prof = UserProfile.objects.exclude(
                id=request.user.userprofile_set.values_list()[0][0])  # exclude himself from invite list
            user_id = request.user.userprofile_set.values_list()[0][0]
            logged_user = UserProfile.objects.get(id=user_id)
            friends = logged_user.friends.all()
            context = {
                'users': users,
                'users_prof': users_prof,
                'logged_user': logged_user,
                'friends' : friends,
            }
            return context
        except:
            users_prof = UserProfile.objects.all()
            context = {
                'users':users,
                'users_prof':users_prof,
            }
            return context
    else:
        context = {
            'users': users,
            'users_prof': users_prof,
        }
        return context


def editBasicFinanceInfo(request,id) :

    if request.method == "POST":
        basicAmt = request.POST.get('amount')
        cuPercent = request.POST.get('percentage')

        existingData = FinanceModel.objects.filter(project_id = id)
        
        if existingData:
            existingData[0].amtreceived = basicAmt
            existingData[0].cupercentage = cuPercent
            existingData[0].save()
        else :
            projDetails = Project.objects.get(id = id)  
            savebasicinfo = FinanceModel()
            savebasicinfo.project_id = projDetails
            savebasicinfo.amtreceived = basicAmt
            savebasicinfo.cupercentage = cuPercent
            savebasicinfo.save()

    return redirect(f'/projects/projects/project/{id}')


def addIncome(request, id) :
    if request.method == "POST":
        particular = request.POST.get('particular')
        amt = request.POST.get('amount')
        tempDict = {
            "particular": particular,
            "amount": amt,
        }

        existingFinance = FinanceModel.objects.filter(project_id = id)
        if existingFinance:
            # saving when its already there
            if not existingFinance[0].incomes:
                # when income is empty
                tempDict["id"] = 1
                incomeJson = json.dumps(tempDict)
                incomeArr = []
                incomeArr.append(incomeJson)
                finalDict = {'add': incomeArr}
                finalJson = json.dumps(finalDict)
                existingFinance[0].incomes = finalJson
                existingFinance[0].save()

            else:
                # when income already exists
                existingIncomeData = json.loads(existingFinance[0].incomes) #dictionary
                newIncomeDict = existingIncomeData['add']
                tempDict["id"] = int(json.loads(newIncomeDict[len(newIncomeDict) - 1])["id"]) + 1
                tempDict = json.dumps(tempDict)
                newIncomeDict.append(tempDict)
                finalDict = {'add': newIncomeDict}
                existingFinance[0].incomes = json.dumps(finalDict)
                existingFinance[0].save()
        
        else:
            # saving a new row
            projDetails = Project.objects.get(id = id)
            tempDict["id"] = 1
            incomeJson = json.dumps(tempDict)
            incomeArr = []
            incomeArr.append(incomeJson)
            finalDict = {'add': incomeArr}
            finalJson = json.dumps(finalDict)
            saveIncome = FinanceModel()
            saveIncome.incomes = finalJson
            saveIncome.project_id = projDetails
            saveIncome.save()
    return redirect(f'/projects/projects/project/{id}')


def addExpense(request,id) :
    if request.method == "POST":
        particular = request.POST.get('particular')
        amt = request.POST.get('amount')
        tempDict = {
            "particular": particular,
            "amount": amt,
        }

        existingExpense = FinanceModel.objects.filter(project_id = id)
        if existingExpense:
            # saving when its already there
            if not existingExpense[0].expenses:
                # when expense is empty
                tempDict["id"] = 1
                expenseJson = json.dumps(tempDict)
                expenseArr = []
                expenseArr.append(expenseJson)
                finalDict = {'less': expenseArr}
                finalJson = json.dumps(finalDict)
                existingExpense[0].expenses = finalJson
                existingExpense[0].save()

            else:
                # when expense already exists
                existingExpenseData = json.loads(existingExpense[0].expenses)
                newExpenseDict = existingExpenseData['less']
                tempDict["id"] = int(json.loads(newExpenseDict[len(newExpenseDict) - 1])["id"]) + 1
                tempDict = json.dumps(tempDict)
                newExpenseDict.append(tempDict)
                finalDict = {'less': newExpenseDict}
                existingExpense[0].expenses = json.dumps(finalDict)
                existingExpense[0].save()
        
        else:
            # saving a new row
            projDetails = Project.objects.get(id = id)
            tempDict["id"] = 1
            expenseJson = json.dumps(tempDict)
            expenseArr = []
            expenseArr.append(expenseJson)
            finalDict = {'less': expenseArr}
            finalJson = json.dumps(finalDict)
            saveExpense = FinanceModel()
            saveExpense.expenses = finalJson
            saveExpense.project_id = projDetails
            saveExpense.save()

    return redirect(f'/projects/projects/project/{id}')


def addProfessor(request, id) :
    if request.method == "POST":
        profname = request.POST.get('name')
        disburseRatio = request.POST.get('ratio')
        desc = request.POST.get('desc')
        tempDict= {
            "Professor": profname,
            "ratio": disburseRatio,
            "desc": desc,
        }

        existingProf = FinanceModel.objects.filter(project_id = id)
        if existingProf:
            # saving when its already there
            if not existingProf[0].professor:
                # when income is empty
                tempDict["id"] = 1
                profJson = json.dumps(tempDict)
                profArr = []
                profArr.append(profJson)
                finalDict = {'professors': profArr}
                finalJson = json.dumps(finalDict)
                existingProf[0].professor = finalJson
                existingProf[0].save()

            else:
                # when income already exists
                existingProfData = json.loads(existingProf[0].professor)
                newProfDict = existingProfData['professors']
                tempDict["id"] = int(json.loads(newProfDict[len(newProfDict) - 1])["id"]) + 1
                tempDict = json.dumps(tempDict)
                newProfDict.append(tempDict)
                finalDict = {'professors': newProfDict}
                existingProf[0].professor = json.dumps(finalDict)
                existingProf[0].save()
        
        else:
            # saving a new row
            projDetails = Project.objects.get(id = id)
            tempDict["id"] = 1
            profJson = json.dumps(tempDict)
            profArr = []
            profArr.append(profJson)
            finalDict = {'professors': profArr}
            finalJson = json.dumps(finalDict)
            saveProfessor = FinanceModel()
            saveProfessor.professor = finalJson
            saveProfessor.project_id = projDetails
            saveProfessor.save()

    return redirect(f'/projects/projects/project/{id}')


def editExpenseInfo(request, id, eid):
    # Expense Information Edit Code Here
    if request.method == "POST":
        particular = request.POST.get('particular')
        amt = request.POST.get('amount')

        tempDict = {
            "particular": particular,
            "amount": amt,
            "id": eid,
        }

        financeExpense = FinanceModel.objects.get(project_id = id)
        existingexpenses = json.loads(financeExpense.expenses)['less']
    
        for i in range(len(existingexpenses)):
            updateExpense = json.loads(existingexpenses[i])
            if updateExpense['id'] == eid:
                existingexpenses[i] = json.dumps(tempDict)
                break

        updatedExpenseDict = {'less': existingexpenses} 

        financeExpense.expenses = json.dumps(updatedExpenseDict)
        financeExpense.save()

    return redirect(f'/projects/projects/project/{id}')


def editIncomeInfo(request, id, iid):
    # Income Information Edit Code Here
    if request.method == "POST":
        particular = request.POST.get('particular')
        amt = request.POST.get('amount')

        tempDict = {
            "particular": particular,
            "amount": amt,
            "id": iid,
        }

        finance = FinanceModel.objects.get(project_id = id)
        
        existingincomes = json.loads(finance.incomes)['add']
    
        for i in range(len(existingincomes)):
            updateIncome = json.loads(existingincomes[i])
            if updateIncome['id'] == iid:
                existingincomes[i] = json.dumps(tempDict)
                break

        updatedIncomeDict = {'add': existingincomes}

        finance.incomes = json.dumps(updatedIncomeDict)
        finance.save()

    return redirect(f'/projects/projects/project/{id}')


def editProfessorInfo(request, id, pid):
    # Professor Information Edit Code Here
    if request.method == "POST":
        profname = request.POST.get('name')
        disburseRatio = request.POST.get('ratio')
        desc = request.POST.get('desc')
        tempDict= {
            "Professor": profname,
            "ratio": disburseRatio,
            "desc": desc,
            "id": pid,
        }

        financeProf = FinanceModel.objects.get(project_id = id)
        existingProf = json.loads(financeProf.professor)['professors']
    
        for i in range(len(existingProf)):
            updateProf = json.loads(existingProf[i])
            if updateProf['id'] == pid:
                existingProf[i] = json.dumps(tempDict)
                break

        updatedProfDict = {'professors': existingProf} 

        financeProf.professor = json.dumps(updatedProfDict)
        financeProf.save()
    return redirect(f'/projects/projects/project/{id}')


@allowed_users(allowed_roles=['Admin'])
def AdminUserDelete(request,id):

    uid = id

    # -------------------------------- Team Remove ------------------------------- #
    teams = Team.objects.filter(assign = uid).values_list()
    teamslist = []
    for t in teams:
        teamslist.append(t[0])
    
    for teamid in teamslist:
        team = Team.objects.get(id = teamid)
        teamname = team.team_name
        team.assign.remove(uid)
        if team.assign.values_list().exists() == False:
            team.delete()
    # -------------------------------- AdminVal User Delete ------------------------------- #
    auser = AdminValidation.objects.get(username = User.objects.get(id = uid))
    auser.delete()
    # ---------------------------- Django User Delete ---------------------------- #
    user = User.objects.get(id = uid)
    user.delete()
    
    return HttpResponseRedirect(reverse('admindashboard'))


@allowed_users(allowed_roles=['Admin'])
def AdminTeamDelete(request,id):
    tid = id
    teamobj = Team.objects.get(id=tid)
    team = Team.objects.filter(id=tid).values_list('assign')
    teammebers = []
    for t in team:
        teammebers.append(t[0])
    for t2 in teammebers:
        teamobj.assign.remove(t2)
    
    projectsid = Project.objects.filter(assign = tid).values_list('id')
    for pid in projectsid:
        project = Project.objects.filter(id = pid[0])
        project[0].assign.remove(tid)
    
    if teamobj.assign.values_list().exists() == False:
        teamobj.delete()

    return HttpResponseRedirect(reverse('admindashboard'))


@allowed_users(allowed_roles=['Admin'])
def AdminProjectDelete(request,id):
    pid = id
    
    # ------------------------------ Delete Finances ----------------------------- #
    finances = FinanceModel.objects.filter(project_id_id = pid)
    for finance in finances:
        finance.delete()
    # ------------------------------- Delete Tasks ------------------------------- #
    tasks = Task.objects.filter(project_id = pid)
    for task in tasks:
        task.delete()
    # ------------------------------ Delete Project ------------------------------ #
    project = Project.objects.get(id = pid)
    project.delete()
    
    return HttpResponseRedirect(reverse('admindashboard'))

def SendAdminRequest(request):
    if request.method == 'POST':
        requesto = RequestModel()
        requesto.name = request.user.username
        requesto.requestmsg = request.POST.get('requestmsg')

    return SignIn(request)
            

@allowed_users(allowed_roles=['Admin'])
def AdminDelRequest(request,id):
    rid = id
    
    requesto = RequestModel.objects.get(id = rid)
    requesto.delete()
    
    return HttpResponseRedirect(reverse('admindashboard'))
