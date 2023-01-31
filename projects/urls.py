from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    path('new-team/', views.newTeam, name='new-team'),
    path('projects/task/<int:id>',views.taskprofile, name='task'),
    path('projects/project/editp/<int:pk>/',views.editproject.as_view(),name='editp'),
    path('projects/project/<int:id>',views.projectprofile, name='Project'),
    path('projects/alltask/',views.taskprofile1, name='task1'),
    path('projects/viewtask/<int:task>',views.viewtask,name='viewtask'),

]