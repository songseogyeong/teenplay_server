from django.urls import path

from wishlist.views import WishListView, WishListAPI, WishListWriteAPI, ReplyWriteAPI, ReplyListAPI, WishListActionAPI, \
    ReplyActionAPI, WishlistLikeAPIView

app_name = 'wishlist'

urlpatterns = [
    path('list/', WishListView.as_view(), name='main'),
    path('write/', WishListWriteAPI.as_view(), name='write'),
    path('list/<int:page>/', WishListAPI.as_view(), name='list'),
    path('reply/write/', ReplyWriteAPI.as_view(), name='apply-write'),
    path('reply/list/', ReplyListAPI.as_view(), name='apply-list'),
    path('wishlist/<int:wishlist_id>/', WishListActionAPI.as_view()),
    path('reply/<int:reply_id>/', ReplyActionAPI.as_view()),
    path('select/like/api/<int:wishlist_id>/<int:memberId>/<str:displayStyle>/', WishlistLikeAPIView.as_view())
]