from django.shortcuts import render
from django.http import HttpResponse
from consultancy2.decorators import *


@allowed_users(allowed_roles=["Finance Manager"])
def finance(request):
    return render(request, "financeHome.html")