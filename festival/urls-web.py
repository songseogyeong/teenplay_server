from django.contrib import admin
from django.urls import path, include

from festival.views import FestivalListWebView, FestivalListWebAPI, FestivalDetailtWebView, FestivalDetailtWebAPI

app_name = 'festival'

urlpatterns = [
    # list 페이지로 이동 후 list 페이지 경로 가져오기
    path('list/', FestivalListWebView.as_view(), name='festival-list'),
    path('list/api/', FestivalListWebAPI.as_view(), name='festival-list-api'),
    # detail 페이지 이동 후 detail 페이지 경로 가져오기
    path('detail/', FestivalDetailtWebView.as_view(), name='festival-detail'),
    path('detail/api/<int:post>', FestivalDetailtWebAPI.as_view(), name='festival-detail-api'),
]
