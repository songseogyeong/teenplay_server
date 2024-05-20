from django.contrib import admin
from django.urls import path, include

from activity.views import ActivityCreateWebView

app_name = 'app-activity'

urlpatterns = [
    path('create/', ActivityCreateWebView.as_view(), name='create'),
]
