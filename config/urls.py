# config/urls.py

from django.urls import path, include
from .views import get_module_info, get_user_activity


urlpatterns = [
    path('get-module-info/', get_module_info, name='module_info'),
    path('get-activity/', get_user_activity, name='activity_list_api'),
    ]