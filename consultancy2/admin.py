from django.contrib import admin
from .models import AdminValidation
from .models import Profile  
from .models import Team

admin.site.register(AdminValidation)
admin.site.register(Profile)
admin.site.register(Team)
