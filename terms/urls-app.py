from django.urls import path

from terms.views import ServiceTermsWebView, RefundTermsWebView, PrivacyTermsWebView, MarketingTermsWebView, \
    InformationTermsWebView, EmailTermsWebView, EBankingTermsWebView

app_name = 'app-terms'

urlpatterns = [
    path('service/', ServiceTermsWebView.as_view(), name='service'),
    path('refund/', RefundTermsWebView.as_view(), name='refund'),
    path('privacy/', PrivacyTermsWebView.as_view(), name='privacy'),
    path('marketing/', MarketingTermsWebView.as_view(), name='marketing'),
    path('information/', InformationTermsWebView.as_view(), name='information'),
    path('email/', EmailTermsWebView.as_view(), name='email'),
    path('e-banking/', EBankingTermsWebView.as_view(), name='e-banking')
]