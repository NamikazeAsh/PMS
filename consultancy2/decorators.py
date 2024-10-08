from textwrap import wrap
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render


def unauthorized_users(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                # return HttpResponse("Not authorized to view this page! (\-W-/)")
                return render(request,"errorPage.html")
            
            return view_func(request,*args,**kwargs)
        return wrapper_func
    return decorator
