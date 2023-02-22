from django.contrib import admin
from .models import Project
from .models import Task
from .models import Comment
from .models import ProjectComment
from mptt.admin import MPTTModelAdmin
from .models import Team

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', ]
    list_filter = ['name', 'company', ]
    search_fields = ['name', 'company', 'status',]
    prepopulated_fields = {'slug':('name',)}

    class Meta:
        model = Project

class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name','project']
    readonly_fields=('slug',)
    list_filter = ['project', ]
    search_fields = ['project']
    
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name']
    


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(ProjectComment, MPTTModelAdmin)
admin.site.register(Team, TeamAdmin)