from django.urls import path, include

from member.views import MemberLoginWebView, MemberJoinWebView, MypageInfoWebView, MypageDeleteWebView, \
    MypageLetterWebView, MypageWriteAPIWebView, MypageListAPIWebView, MypageDeleteAPIWebView, MypageCheckAPIWebViewMa, \
    MypageAlramView, MypageAlramAPIView, MypageAlramDeleteAPIView, MypageTeenchinview, MypageTeenchinAPIview, \
    MemberAlarmCountAPI, MypageTeenchindeleteview, MypageTeenchinLetterAPIview, MapagePaymentView, MypagePayListAPIVIEW, \
    MypagePayDeleteAPIVIEW, MypageReplyView, MypageReplyAPIVIEW, MypageReplyDeleteAPIVIEW, TeenChinAPI, \
    MypageActivityListView, MypageActivityListAPI, MypageMemberView, MypageNoticeView, MypageNoticeAPI, \
    MypageNoticeCreateView, MypageSettingView, MypageMemberListAPI, MypageMemberStatusAPI, \
    ClubAlarmManageAPI, MypageActivityLikeAPIVIEW, MypageActivityAPIVIEW, MypageActivityVIEW, ActivityManagentView, \
    ActivityListAPIView, ActivityMemberView, ActivityMemberListAPIView, ActivityMemberUpdateAPIView, \
    ActivityMemberWriteAPI, ActivityEditView, MypageNoticeModifyView, MypageSendLetterAPI, \
    MypageMyClubView, MypageMyClubAPI, MypageClubDeleteView, MypageMyClubAlarmStatusAPI, \
    MypageWishlistAPIView, MypageWishlistDeleteAPIView, MypageWishlistWebView, MypageNoticeDeleteAPI

app_name = 'member'

urlpatterns = [
    path('login/', MemberLoginWebView.as_view(), name='login'),
    path('join/', MemberJoinWebView.as_view(), name='join'),
    path('mypage-info/', MypageInfoWebView.as_view(), name='mypage-info'),
    path('mypage-delete/', MypageDeleteWebView.as_view(), name='mypage-delete'),
    path('mypage-letter/', MypageLetterWebView.as_view(), name='mypage-letter'),
    path('mypage-apiletter/', MypageWriteAPIWebView.as_view(), name='mypage-apiletter'),
    path('mypage-letter/<int:member_id>/<int:page>/', MypageListAPIWebView.as_view(), name='mypage-apilist'),
    path('mypage-letter/<int:letter_id>/', MypageDeleteAPIWebView.as_view(), name='mypage-apidelete'),
    path('mypage-letterapi/', MypageCheckAPIWebViewMa.as_view(), name='mypage-apicheck'),
    path('mypage-alram/', MypageAlramView.as_view(), name='mypage-alram'),
    path('mypage-alram/<int:member_id>/<int:page>/', MypageAlramAPIView.as_view(), name='mypage-apialram'),
    path('mypage-alram/<int:alram_id>/', MypageAlramDeleteAPIView.as_view(), name='mypage-apideletealram'),
    path('mypage-teenchin/', MypageTeenchinview.as_view(), name='mypage-teenchin'),
    path('mypage-teenchin/<int:member_id>/<int:page>/', MypageTeenchinAPIview.as_view(), name='mypage-apiteenchin'),
    path('alarms/api/', MemberAlarmCountAPI.as_view(), name='alarms-count-api'),
    path('mypage-teenchin/<int:member_id>/<int:page>/', MypageTeenchinAPIview.as_view(), name='mypage-apiteenchin'),
    path('mypage-teenchin/<int:friend_id>/', MypageTeenchindeleteview.as_view(), name="mypage-apiteenchindelete"),
    path('mypage-teenchinapi/', MypageTeenchinLetterAPIview.as_view(), name="mypage-teenchinletter"),
    path('mypage-payment/', MapagePaymentView.as_view(), name='mapage-payment'),
    path('mypage-payment/<int:member_id>/<int:page>/', MypagePayListAPIVIEW.as_view(), name='mypage-paymentapl'),
    path('mypage-payment/api/', MypagePayDeleteAPIVIEW.as_view(), name="mypage-paydelete"),
    path('mypage-reply/', MypageReplyView.as_view(), name="mypage-reply"),
    path('mypage-reply/<int:member_id>/<int:page>/', MypageReplyAPIVIEW.as_view(), name="mypage-apireply"),
    path('mypage-reply/<str:reply_id>/', MypageReplyDeleteAPIVIEW.as_view(), name="mypage-deletereply"),
    path('teenchin/api/', TeenChinAPI.as_view(), name="teenchin-api"),
    path('club-alarm/api/', ClubAlarmManageAPI.as_view(), name="club-alarm-manage-api"),
    path('mypage-my-club/', MypageMyClubView.as_view(), name="mypage-my-club"),
    path('mypage-my-club/api/', MypageMyClubAPI.as_view(), name="mypage-my-club-api"),
    path('mypage-my-club-alarm/<int:club_id>/', MypageMyClubAlarmStatusAPI.as_view(), name="mypage-my-club-alarm-api"),
    path('mypage-club/<int:club_id>/', MypageActivityListView.as_view(), name="mypage-club"),
    path('mypage-club-delete/<int:club_id>/', MypageClubDeleteView.as_view(), name="mypage-club-delete"),
    path('mypage-activity-list/<int:club_id>/', MypageActivityListAPI.as_view(), name="mypage-activity-list-api"),
    path('mypage-member/<int:club_id>/', MypageMemberView.as_view(), name="mypage-member"),
    path('mypage-member-list/<int:club_id>/', MypageMemberListAPI.as_view(), name="mypage-member-list-api"),
    path('mypage-member-status/<int:club_id>/', MypageMemberStatusAPI.as_view(), name="mypage-member-status-api"),
    path('mypage-notice/<int:club_id>/', MypageNoticeView.as_view(), name="mypage-notice"),
    path('mypage-notice-list/<int:club_id>/', MypageNoticeAPI.as_view(), name="mypage-notice-list-api"),
    path('mypage-notice-delete/<int:club_id>/', MypageNoticeDeleteAPI.as_view(), name="mypage-notice-list-api"),
    path('mypage-notice-write/<int:club_id>/', MypageNoticeCreateView.as_view(), name="mypage-create"),
    path('mypage-notice-modify/<int:club_id>/', MypageNoticeModifyView.as_view(), name="mypage-modify"),
    path('mypage-send-letter/api/', MypageSendLetterAPI.as_view(), name="mypage-send-letter-api"),
    path('mypage-setting/<int:club_id>/', MypageSettingView.as_view(), name="mypage-setting"),
    path('mypage-activity/', MypageActivityVIEW.as_view(), name="mypage-activity"),
    path('mypage-activity/<int:member_id>/<int:page>/', MypageActivityAPIVIEW.as_view(), name="mypage-apiactivity"),
    path('mypage-activity/<int:activity_id>/', MypageActivityLikeAPIVIEW.as_view(), name="mypage-apiactivitylike"),
    path('activity/', ActivityManagentView.as_view(), name="management-activity"),
    path('activity/<int:member_id>/<int:page>/', ActivityListAPIView.as_view(), name="management-aipactivity"),
    path('activity-member/', ActivityMemberView.as_view(), name="management-activitymember"),
    path('activity-member/<int:member_id>/<int:page>/<int:activity_id>/', ActivityMemberListAPIView.as_view(),
         name="management-aipactivitymember"),
    path('activity-member/<int:activity_member_id>/<int:activity_id>/', ActivityMemberUpdateAPIView.as_view(),
         name="managment-apiupdateactivitymember"),
    path('activity-member/api/', ActivityMemberWriteAPI.as_view(), name="managment-apideleteactivitymember"),
    path('activity-edit/', ActivityEditView.as_view(), name="managment-edit"),
    path('mypage-wishlist/', MypageWishlistWebView.as_view(), name='mypage-wishlist'),
    path('mypage-wishlist/<int:member_id>/<int:page>/', MypageWishlistAPIView.as_view(), name='mypage-wishlistapi'),
    path('mypage-wishlist/<int:wishlist_id>/', MypageWishlistDeleteAPIView.as_view(), name='mypage-wishlist-delete')
]
