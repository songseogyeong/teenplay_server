from django.contrib import admin
from django.urls import path, include

from notice.views import NoticeListWebView, NoticeListAPIView

app_name = 'notice'

urlpatterns = [
    path('list/', NoticeListWebView.as_view(), name='notice-list'),
    path('list/<int:page>', NoticeListAPIView.as_view(), name='notice-list-api')
]
