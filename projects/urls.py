from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    path('projects/task/<int:id>',views.taskprofile, name='task'),
    # path('projects/edittask/<slug:pk>',views.edittask.as_view(),name='edittask'),
    path('projects/alltask/',views.taskprofile1, name='task1'),
    path('projects/viewtask/<int:task>',views.viewtask,name='viewtask'),
    # path('projects/viewtask/<int:id>',views.viewtask,name='view-task'),
    # path('projects/<slug:post>/', views.post_single, name='post_single'),

    # path('projects/projectprofile/<int:id>',views.ProjectProfile,name='project-profile'),

]