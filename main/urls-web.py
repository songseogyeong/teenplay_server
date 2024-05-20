from django.urls import path

from main.views import RecentSearchKeywordAPI, RecentSearchKeywordDeleteAllAPI, RealTimeSearchAPI

app_name = 'search'

urlpatterns = [
    path('recent-keywords/api/', RecentSearchKeywordAPI.as_view(), name='recent-keywords'),
    path('recent-keywords-delete-all/api/', RecentSearchKeywordDeleteAllAPI.as_view(), name='recent-keywords-delete-all'),
    path('realtime-search/api/', RealTimeSearchAPI.as_view(), name='realtime-search'),
]

