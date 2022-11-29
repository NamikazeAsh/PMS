from django.shortcuts import render

# Create your views here.
def index(request):
    render(request,'srintern/tempsrintern.html')