from django.contrib import admin
from .models import AdminValidation

class AdminValidationAdmin(admin.ModelAdmin):
    list_display = ['username','firstname','lastname']
    list_display = ['username','firstname','lastname','campus','role']
    search_fields = ['username','firstname','lastname','campus','role']

    class Meta:
        model = AdminValidation

admin.site.register(AdminValidation,AdminValidationAdmin)