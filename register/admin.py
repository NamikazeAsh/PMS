from django.contrib import admin
from .models import Company
from .models import UserProfile



class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name','email','city','found_date']
    search_fields = ['name','city']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company',]


    


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


