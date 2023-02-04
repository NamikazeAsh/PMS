from django.shortcuts import render
from .models import Event

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

def deleteMilestone(request,mileid):

    userid = request.user.id
    eventmod = Event.objects.filter(id = mileid)
    eventmod.delete()
    temp = findtemp(request)
    object_list = Event.objects.filter(user_id = userid)
    
    return render(request,"calendarapp/events_list.html",{'temp':temp,'object_list':object_list})