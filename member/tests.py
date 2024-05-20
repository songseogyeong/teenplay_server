from django.test import TestCase

from activity.models import Activity
from club.models import Club, ClubMember, ClubNotice
from member.models import Member


class MemberTest(TestCase):
    club = Club.objects.get(id=11)
    member = Member.objects.get(id=6)
    # data = {
    #     'club': club,
    #     'member': member,
    #     'status': 1,
    #     'alarm_status':1
    # }
    #
    # ClubMember.objects.create(**data)

    # for i in range(4):
    #     data = {
    #         'club': club,
    #         'notice_title': f'xptmdxm{i}',
    #         'notice_content': f'sodydxotmxm{i}',
    #         'status': 1
    #     }
    #
    #     ClubNotice.objects.create(**data)


