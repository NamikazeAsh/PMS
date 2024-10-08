from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
from django.utils import timezone
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from itertools import chain
from consultancy2.models import *
from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm

from django.core.mail import send_mail

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

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "register:login"
    model = Event
    template_name = "calendarapp/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        var = findtemp()
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        context["temp"] = var
        return context


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "calendarapp/event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "calendarapp/event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        var = findtemp(self.request)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        context["temp"] = var
        return context


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    users2 = AdminValidation.objects.all()
    eventmember = EventMember.objects.filter(event=event)
    var = findtemp(request)
    context = {"event": event, "eventmember": eventmember,
    'temp':var,'users2':users2}
    return render(request, "calendarapp/event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    event = Event.objects.get(id=event_id)
    member_count = EventMember.objects.filter(event=event).count()
    is_member_warning = False
    
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            user = forms.cleaned_data["user"]
            member = EventMember.objects.filter(event=event, user=user)
            if member.exists():
                is_member_warning = True
            else:
                EventMember.objects.create(event=event, user=user)
                return event_details(request,event_id)

    var = findtemp(request)
    context = {
        "form": forms,
        "temp": var,
        "event": event,
        "member_count": member_count,
        "is_member_warning": is_member_warning,
    }
    return render(request, "calendarapp/add_member.html", context)



class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "calendarapp/event_delete.html"
    
    def get_success_url(self):
        event_id = self.object.event_id
        return reverse_lazy("calendarapp:event-detail", kwargs={"event_id": event_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        var = findtemp(self.request)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        context["temp"] = var
        return context
    



class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "register:login"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        id = request.user.id
        events = Event.objects.get_all_events(user=request.user)
        k = []
        s = EventMember.objects.all()
        for item in s:
            if item.user == request.user:
                k.append(item.event)
        eve = Event.objects.get_running_events(user=request.user)
        m =[]
        event_list = []
        for event in events:
            event_list.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        for event in k:
            event_list.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
            if event.end_time.date() >= datetime.datetime.now(tz=timezone.utc).date():
                m.append(
                    {
                        "id": event.id,
                        "title": event.title,
                        "start_time": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end_time": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                )
        var = findtemp(request)
        events_month = list(chain(eve,m))
        context = {"form": forms, "events": event_list,"events_month": events_month,'temp':var,}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        var = findtemp(request)
        context = {"form": forms,'temp':var,}
        

        
        return render(request, self.template_name, context)
