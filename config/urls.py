# config/urls.py

from django.urls import path, include
from .views import get_modules_view, get_user_activity


urlpatterns = [
    path('get-modules/', get_modules_view, name='modules_api'),
    path('get-activity/', get_user_activity, name='activity_list_api'),
    ]