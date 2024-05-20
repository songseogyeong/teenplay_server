from django.shortcuts import render
from django.views import View


class ServiceTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/service-terms-web.html')


class RefundTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/refund-terms-web.html')


class PrivacyTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/privacyprovision-web.html')


class MarketingTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/marketing-terms-web.html')


class InformationTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/information-web.html')


class EmailTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/email-terms-web.html')


class EBankingTermsWebView(View):
    def get(self, request):
        return render(request, 'terms/web/e-banking-terms-web.html')
