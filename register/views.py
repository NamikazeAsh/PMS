from django.shortcuts import render,get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from projects.models import Task
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegistrationForm,ProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from consultancy2.models import *
from django.contrib.auth.decorators import login_required
from consultancy2.decorators import allowed_users


# Create your views here.

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


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            user = form.save()
            created = True
            var = findtemp(request)
            context = {'created' : created,
            'temp':var,}
            return render(request, 'register/reg_form.html', context)
        else:
            return render(request, 'register/reg_form.html', context)
    else:
        form = RegistrationForm()
        var = findtemp(request)
        context = {
            'form' : form,
            'temp':var,
        }
        return render(request, 'register/reg_form.html', context)


def usersView(request):
    users = UserProfile.objects.all()
    users2 = AdminValidation.objects.all()
    tasks = Task.objects.all()
    var = findtemp(request)
    context = {
        'users': users,
        'users2':users2,
        'tasks': tasks,
        'temp':var,
    }
    return render(request, 'register/users.html', context)



def user_view(request, profile_id):
    request.session['profile_id'] = profile_id
    user = UserProfile.objects.get(user_id=profile_id)
    prof=request.user.groups.filter(name='Professor')
    srintern=request.user.groups.filter(name='Sr Intern')
    user_val = AdminValidation.objects.get(username=user.user.username)
    form = ProfileForm(request.POST or None,request.FILES or None,instance=user_val)
    if form.is_valid():
        form.save()
    var = findtemp(request)
    baseurl = "core"
    context = {
        'baseurl' : baseurl,
        'user_view' : user,
        'user_val' : user_val,
        'temp':var,
        'prof':prof,
        'srintern':srintern,
        'form':form,
    }
    return render(request, 'register/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Sr Intern','Professor'])
def deltask(request,task):
    profile_id = request.session['profile_id']
    task=get_object_or_404(Task, id=task)
    task.assign.remove(profile_id)
    if task.assign.exists() == False:
        task.delete()
    uid=profile_id
    return redirect('register:user',uid)

