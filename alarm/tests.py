from django.test import TestCase

from activity.models import ActivityReply, Activity
from alarm.models import Alarm
from club.models import Club


class ActivityReplyAlarmTests(TestCase):
    pass
    # data = {
    #     'reply_content': '알람 테스트용 댓글1',
    #     'activity_id': '11',
    #     'member_id': 5
    # }
    #
    # activity_reply = ActivityReply.objects.create(**data)
    #
    # # 모임장에게 활동 상세글 댓글 알림 전송
    # activity = Activity.enabled_objects.filter(id=data['activity_id']).first()
    # club = Club.enabled_objects.filter(id=activity.club.id).first()
    # alarm_data = {
    #     'target_id': activity.id,
    #     'alarm_type': 2,
    #     'sender_id': activity_reply.member.id,
    #     'receiver_id': club.member.id,
    # }
    # alarm = Alarm.objects.create(**alarm_data)
    # print(alarm.__dict__)
