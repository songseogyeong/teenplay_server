from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from member.models import Member
from member.serializers import MemberSerializer


class OAuthLoginView(View):

    def get(self, request):
        user = SocialAccount.objects.get(user=request.user)
        provider = user.provider
        data = user.extra_data

        if provider == 'kakao':
            member_email = data['kakao_account']['email']
            member_name = data['properties']['nickname']
        else:
            member_email = data['email']
            member_name = data['name']

        # user = User.objects.filter(email=member_email)
        # if user.exists():
        #     user.first().delete()

        data = {
            'member_type': provider,
            'member_email': member_email,
            'member_nickname': member_name
        }

        if not Member.enabled_objects.filter(**data).exists():
            return redirect(f'/member/join?type={provider}&email={member_email}&name={member_name}')

        member = Member.enabled_objects.filter(**data)

        request.session['member'] = MemberSerializer(member.first()).data
        path = "/"
        previous_uri = request.session.get('previous_uri')
        if previous_uri is not None:
            path = previous_uri
            del request.session['previous_uri']

        return redirect(path)

