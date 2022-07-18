"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# used by reverse lookup funtion to get full url -> app_name:url_name, so user:create
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
