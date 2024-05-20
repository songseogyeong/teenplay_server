from django.contrib import admin
from django.urls import path, include

from festival.views import FestivalListAppView, FestivalListAppAPI, FestivalDetailAppView, FestivalDetailAppAPI

app_name = 'app-festival'

urlpatterns = [
    # list 페이지로 이동 후 list 페이지 경로 가져오기
    path('list/', FestivalListAppView.as_view(), name='festival-list'),
    path('list/api/<int:page>', FestivalListAppAPI.as_view(), name='festival-list-api'),
    # detail 페이지 이동 후 detail 페이지 경로 가져오기
    path('detail/', FestivalDetailAppView.as_view(), name='festival-detail'),
    path('detail/api/<int:post>', FestivalDetailAppAPI.as_view(), name='festival-detail-api'),
]
