from django.contrib import admin
from .models import Company,Team
from .models import UserProfile
from .models import Invite


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name','email','city','found_date']
    search_fields = ['name', 'social_name','city']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company',]

class InviteAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'invited',]
    search_fields = ['inviter', 'invited',]
    # list_filter = ['inviter', 'invited,']

# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(Team)
