from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('projects/edit_project/<int:id>', views.edit_project, name='edit-project'),
    path('team-views/',views.teams,name='teams'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    path('projects/edit_task/<int:id>', views.edit_task, name='edit-task'),
    path('new-team/', views.newTeam, name='new-team'),
    path('projects/task/<int:id>',views.taskprofile, name='task'),
    path('projects/alltask/',views.taskprofile1, name='task1'),
    path('projects/deletetask/<int:task>',views.deltask,name='deletetask'),
    path('projects/project/<int:id>',views.ProjectProfile, name='project-profile'),
    path('projects/deletecomment/<int:id>',views.deletecomment, name='delete-comment'),
    path('projects/downloadprojreport/<int:id>',views.DownloadProjectReport,name='DownloadProject'),
    path('projects/downloadallprojreport/',views.DownloadAllProjectReport,name='DownloadAllProject'),
    path('projects/uploadprojdoc/<int:id>',views.UploadProjectDocs,name='UploadProjDocs'),
    path('projects/uploadrefprojdoc/<int:id>',views.UploadRefProjectDocs,name='UploadRefProjDocs'),
    path('team-views/editteam/<str:teamname>',views.editTeamInfo,name='editTeamInfo'),
    path('team-views/deleteteam/<str:teamname>',views.deleteTeamInfo,name='deleteTeamInfo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)