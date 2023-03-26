from django.shortcuts import render

# Create your views here.
from multiprocessing import context
from projects.models import Project,Team
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm

from consultancy2 import models
from register.forms import RegistrationForm
from .models import AdminValidation, SignInInsert,HourVal
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

import datetime
import json

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
        return 'consultant/tempprof.html'
    elif request.user.groups.filter(name='Head Consultant').exists():
        return 'consultant/tempprof.html'

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
            return render(request,'srintern/tempsrintern.html')
        elif request.user.groups.filter(name='Lead Consultant').exists():
            return render(request,'consultant/tempprof.html')
        elif request.user.groups.filter(name='Head Consultant').exists():
            return render(request,'consultant/tempprof.html')
        else:
            return render(request,'admindashboard.html')
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
                        return render(request,'consultant/tempprof.html')
                    elif request.user.groups.filter(name='Head Consultant').exists():
                        return render(request,'consultant/tempprof.html')
                    elif request.user.groups.filter(name='Finance Manager').exists():
                        return render(request,'financeHome.html')
                    else:
                        return render(request,'admindashboard.html')

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
    print(user)
    
    up = UserProfile.objects.create(user=user)
    up.save()
    print("up saved")
    
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
    if request.user.groups.filter(name='Intern').exists():
        return render(request,'intern/tempintern.html')
    elif request.user.groups.filter(name='Sr Intern').exists():
        return render(request,'srintern/tempsrintern.html')
    elif request.user.groups.filter(name='Professor').exists():
        return render(request,'srintern/tempsrintern.html')
    elif request.user.groups.filter(name='Lead Consultant').exists():
        return render(request,'consultant/tempprof.html')
    elif request.user.groups.filter(name='Head Consultant').exists():
        return render(request,'consultant/tempprof.html')
    else:
        return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern'])
def TempSrIntern(request):
    return render(request,'srintern/tempprof.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern','Intern','Professor','Lead Consultant','Head Consultant'])
def UsersProfile(request):
    return render(request,"profile.html",context)

@login_required(login_url='login')
def ProjectProfile(request,id):
    
    return render(request,"projectprofile.html",context)

@login_required(login_url='login')
def UserHourTracking(request):
    if request.user.groups.filter(name='Intern').exists():
        return redirect('user-hours-i')
    elif request.user.groups.filter(name='Sr Intern').exists():
        return redirect('user-hours-i')
    elif request.user.groups.filter(name='Professor').exists():
        return redirect('user-hours-p')
    elif request.user.groups.filter(name='Head Consultant').exists():
        return redirect('user-hours-p')
    elif request.user.groups.filter(name='Lead Consultant').exists():
        return redirect('user-hours-p')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern','Intern'])
def UserHourTrackingIntern(request):
    
    if request.method == "POST":

        saverecord = HourVal()
        saverecord.email = request.user.email
        saverecord.hours_claimed = request.POST.get('hours')
        saverecord.date_claimed = datetime.datetime.now()
        saverecord.team = request.POST.get('team')
        saverecord.description = request.POST.get('description')
        saverecord.save()
        
        # if request.POST.get('freehouri') == True:
        #     print("checked")
        # else:
        #     print("not checked")
        
        return redirect('signup')
        
    var = findtemp(request)
    
    freehouro = AdminValidation.objects.get(email = request.user.email)
    print(freehouro)
    
    context = {
        "temp": var,
        "freehourso":freehouro,
    }
    
    return render(request,"userhour_intern.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Professor','Head Consultant','Lead Consultant'])
def UserHourTrackingProfessor(request):

    if request.method == "POST":
        
        uhour = request.POST.get('hours')
        
        valusers = AdminValidation.objects.get(email = request.user.email)
        updhour = valusers.hours
        newhour = updhour + int(uhour)
        
        valusers.hours = newhour
        valusers.save()
        
        return redirect('signup') #home/signup autodirect home
        
    details = HourVal.objects.all()
    freehouro = AdminValidation.objects.get(email = request.user.email)
    print(freehouro)
    
    var = findtemp(request)
    context = {
        "temp": var,
        "details":details,
        "freehourso":freehouro,
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
    
    print("Successfully updated!")    
    
    return HttpResponseRedirect(reverse('user-hours-p'))

@login_required(login_url='login')
def UserHourTrackingDeny(request,id):
    
    delentry = HourVal.objects.get(id=id)
    delentry.delete()
    return HttpResponseRedirect(reverse('user-hours-p'))


@login_required(login_url='admin:login')
@allowed_users(allowed_roles=['Admin'])
def AdminDashboard(request):
    projects = Project.objects.all()
            
    # context = {"teams":teams,"projects":projects}
    return render(request,"admindashboard.html")



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

    # newFinanceData = FinanceModel.objects.get(project_id = id)

    # # return ProjectProfile(request, id)
    # return projects(request)
    # return render(request,"projectprofile.html",{'financeData': newFinanceData})
    return render(request,"projectprofile.html",context)

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
                incomeJson = json.dumps(tempDict)
                incomeArr = []
                incomeArr.append(incomeJson)
                finalDict = {'add': incomeArr}
                finalJson = json.dumps(finalDict)
                existingFinance[0].incomes = finalJson
                existingFinance[0].save()

            else:
                # when income already exists
                existingIncomeData = json.loads(existingFinance[0].incomes)
                newIncomeDict = existingIncomeData['add']
                tempDict = json.dumps(tempDict)
                newIncomeDict.append(tempDict)
                finalDict = json.dumps(newIncomeDict)
                existingFinance[0].incomes = finalDict
                existingFinance[0].save()
        
        else:
            # saving a new row
            projDetails = Project.objects.get(id = id)
            incomeJson = json.dumps(tempDict)
            incomeArr = []
            incomeArr.append(incomeJson)
            finalDict = {'add': incomeArr}
            finalJson = json.dumps(finalDict)
            saveIncome = FinanceModel()
            saveIncome.incomes = finalJson
            saveIncome.project_id = projDetails
            saveIncome.save()

    # newFinanceData = FinanceModel.objects.get(project_id = id)

    # # return ProjectProfile(request, id)
    # return render(request,"projectprofile.html",{'financeData': newFinanceData})
    return render(request,"projectprofile.html",context)

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
                # when income is empty
                expenseJson = json.dumps(tempDict)
                expenseArr = []
                expenseArr.append(expenseJson)
                finalDict = {'less': expenseArr}
                finalJson = json.dumps(finalDict)
                existingExpense[0].expenses = finalJson
                existingExpense[0].save()

            else:
                # when income already exists
                existingExpenseData = json.loads(existingExpense[0].expenses)
                newExpenseDict = existingExpenseData['less']
                tempDict = json.dumps(tempDict)
                newExpenseDict.append(tempDict)
                finalDict = json.dumps(newExpenseDict)
                existingExpense[0].expenses = finalDict
                existingExpense[0].save()
        
        else:
            # saving a new row
            projDetails = Project.objects.get(id = id)
            expenseJson = json.dumps(tempDict)
            expenseArr = []
            expenseArr.append(expenseJson)
            finalDict = {'less': expenseArr}
            finalJson = json.dumps(finalDict)
            saveExpense = FinanceModel()
            saveExpense.expenses = finalJson
            saveExpense.project_id = projDetails
            saveExpense.save()

    # newFinanceData = FinanceModel.objects.get(project_id = id)
    # # return ProjectProfile(request, id)
    # return render(request,"projectprofile.html",{'financeData': newFinanceData})
    return render(request,"projectprofile.html",context)


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
                tempDict = json.dumps(tempDict)
                newProfDict.append(tempDict)
                finalDict = json.dumps(newProfDict)
                existingProf[0].professor = finalDict
                existingProf[0].save()
        
        else:
            # saving a new row
            projDetails = Project.objects.get(id = id)
            profJson = json.dumps(tempDict)
            profArr = []
            profArr.append(profJson)
            finalDict = {'professors': profArr}
            finalJson = json.dumps(finalDict)
            saveProfessor = FinanceModel()
            saveProfessor.professor = finalJson
            saveProfessor.project_id = projDetails
            saveProfessor.save()

    # newFinanceData = FinanceModel.objects.get(project_id = id)
    # # return ProjectProfile(request, id)
    # return render(request,"projectprofile.html",{'financeData': newFinanceData})
    return render(request,"projectprofile.html",context)
