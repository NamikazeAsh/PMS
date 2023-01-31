from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    path('', views.finance),
    # path('home',views.HomePage,name="home"),
    # path('',views.SignIn,name="signup"),
    # path('login/',views.LogIn,name="login"), 
    # path('logout/',views.LogOut,name="logout"),
    # path('adminval/',views.AdminVal,name="adminval"),
    # path('adminval/approve/<int:id>',views.AdminValAcc,name="adminval-approve"),
    # path('adminval/delete/<int:id>',views.AdminValDel,name="adminval-delete"),
    # path('tempintern',views.TempIntern,name='temp-intern'),
    # path('tempsrintern',views.TempSrIntern,name='temp-srintern'),
    # path('userprofile/',views.UserProfile,name='user-profile'),
    # path('userhours',views.UserHourTracking,name="user-hours"),
    # path('userhours-i',views.UserHourTrackingIntern,name="user-hours-i"),
    # path('userhours-p',views.UserHourTrackingProfessor,name="user-hours-p"),
    # path('userhours-p/approve/<int:id>',views.UserHourTrackingAccept,name="userhour-accept"),
    # path('userhours-p/deny/<int:id>',views.UserHourTrackingDeny,name="userhour-deny"),
    # path('intern/', include('intern.urls', namespace='intern')),
    # path('admindashboard/',views.AdminDashboard,name='admindashboard'),
    # path('register/', include('register.urls', namespace='register')),
    # path('projects/', include('projects.urls', namespace='projects')),
    # path('core/', include('core.urls', namespace='core')),
    # path("calendar/", include("calendarapp.urls")),
    # path('srintern/', include('srintern.urls', namespace='srintern')),
    # path('', include('core.urls', namespace='core')),
    # path('professor/', include('professor.urls', namespace='professor')),
    # path('consultant/', include('consultant.urls', namespace='consultant')),

]
