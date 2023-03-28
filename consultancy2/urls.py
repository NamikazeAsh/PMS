"""consultancy2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('admin/', admin.site.urls),
    path('home',views.HomePage,name="home"),
    path('',views.SignIn,name="signup"),
    path('login/',views.LogIn,name="login"), 
    path('logout/',views.LogOut,name="logout"),
    path('adminval/',views.AdminVal,name="adminval"),
    path('adminval/approve/<int:id>',views.AdminValAcc,name="adminval-approve"),
    path('adminval/delete/<int:id>',views.AdminValDel,name="adminval-delete"),
    path('tempintern',views.TempIntern,name='temp-intern'),
    path('tempsrintern',views.TempSrIntern,name='temp-srintern'),
    path('userprofile/',views.UsersProfile,name='user-profile'),
    path('userhours',views.UserHourTracking,name="user-hours"),
    path('userhours-i',views.UserHourTrackingIntern,name="user-hours-i"),
    path('userhours-p',views.UserHourTrackingProfessor,name="user-hours-p"),
    path('userhours-p/approve/<int:id>',views.UserHourTrackingAccept,name="userhour-accept"),
    path('userhours-p/deny/<int:id>',views.UserHourTrackingDeny,name="userhour-deny"),
    path('intern/', include('intern.urls', namespace='intern')),
    path('admindashboard/',views.AdminDashboard,name='admindashboard'),
    path('register/', include('register.urls', namespace='register')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('core/', include('core.urls', namespace='core')),
    path("calendar/", include("calendarapp.urls")),
    path("finance/", include("finance.urls")),

    path("projects/project/<int:id>/editexpense/<int:eid>", views.editExpenseInfo, name="editBasicFinanceInfo"),
    path("projects/project/<int:id>/editincome/<int:iid>", views.editIncomeInfo, name="editBasicFinanceInfo"),
    path("projects/project/<int:id>/editprofessor/<int:pid>", views.editProfessorInfo, name="editBasicFinanceInfo"),

    path("projects/project/<int:id>/editBasicFinanceInfo", views.editBasicFinanceInfo, name="editBasicFinanceInfo"),
    path("projects/project/<int:id>/addexpense", views.addExpense, name="addExpense"),
    path("projects/project/<int:id>/addincome", views.addIncome, name="addIncome"),
    path("projects/project/<int:id>/addprofessor", views.addProfessor, name="addProfessor"),

    # path('srintern/', include('srintern.urls', namespace='srintern')),
    # path('', include('core.urls', namespace='core')),
    # path('professor/', include('professor.urls', namespace='professor')),
    # path('consultant/', include('consultant.urls', namespace='consultant')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
