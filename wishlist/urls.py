from django.urls import path

from wishlist.views import WishListView, WishListWriteView, WishListAPI

app_name = 'wishlist'

urlpatterns = [
    path('list/', WishListView.as_view(), name='list'),
    path('list/', WishListWriteView.as_view(), name='write'),
    path('wishlist/<int:page>/', WishListAPI.as_view(), name='list-api'),
    # path('reply/<int:page>/', WishListReplyAPI.as_view(), name='reply-api')
]