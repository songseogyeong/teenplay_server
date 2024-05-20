from django.urls import path

from main.views import RecentSearchKeywordAPI

app_name = 'search'

urlpatterns = [
    path('recent-keywords/api/', RecentSearchKeywordAPI.as_view(), name='recent-keywords')
]

