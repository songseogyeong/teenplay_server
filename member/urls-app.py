from django.urls import path, include

from member.views import MemberLoginWebView, MemberJoinWebView

app_name = 'app-member'

urlpatterns = [
    path('login/', MemberLoginWebView.as_view(), name='login'),
    path('join/', MemberJoinWebView.as_view(), name='join'),
]