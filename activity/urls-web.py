from django.contrib import admin
from django.urls import path, include

from activity.views import ActivityCreateWebView, ActivityDetailWebView, ActivityLikeAPI, ActivityReplyAPI, \
    ActivityLikeCountAPI, ActivityListWebView, ActivityListAPI, ActivityCategoryAPI, ActivityJoinWebView, \
    ActivityImageUploadAPI, ActivityMemberCountAPI

app_name = 'activity'

urlpatterns = [
    path('create/', ActivityCreateWebView.as_view(), name='activity-create-web'),
    path('detail/', ActivityDetailWebView.as_view(), name='activity-detail-web'),
    path('replies/api/', ActivityReplyAPI.as_view(), name='activity-reply-api'),
    path('like/', ActivityLikeAPI.as_view(), name='activity-like-api'),
    path('likes/api/', ActivityLikeCountAPI.as_view(), name='activity-like-count-api'),
    path('list/', ActivityListWebView.as_view(), name='activity-list-web'),
    path('lists/api/', ActivityListAPI.as_view(), name='activity-lists-api'),
    path('categories/api/', ActivityCategoryAPI.as_view(), name='activity-categories-api'),
    path('join/', ActivityJoinWebView.as_view(), name='activity-join-web'),
    path('images/api/', ActivityImageUploadAPI.as_view(), name='activity-image-api'),
    path('members/api/', ActivityMemberCountAPI.as_view(), name='activity-member-count-api')
]
