from django.shortcuts import render

# Create your views here.
from multiprocessing import context
from projects.models import Project
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
from register.models import *




import datetime

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
            return render(request,'admindashboard.html')
    else:    
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            context = {'form':form}
            if form.is_valid():
                saverecord = SignInInsert()
                saverecord.email = form.cleaned_data.get("email")
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
    saverecord.password = auser.password
    saverecord.campus = auser.campus
    saverecord.role = auser.role
    saverecord.save()
    
    user = User.objects.create_user(auser.email,auser.email,auser.password)
    user.save()
    print(user)
    
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
def UserProfile(request):
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
        saverecord.save()
        
        if request.POST.get('freehouri') == True:
            print("checked")
        else:
            print("not checked")
        
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
