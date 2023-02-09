from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('new-user/', views.register, name='new-user'),

    path('users/', views.usersView, name='users'),
    # path('users/<int:id>/', views.usersView, name='users'),
    path('users/<int:profile_id>/', views.user_view, name='user'),

]

