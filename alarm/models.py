from django.db import models

from alarm.managers import AlarmManager
from member.models import Member
from teenplay_server.period import Period


class Alarm(Period):
    target_id = models.IntegerField(null=False, blank=False)
    # 0: 읽음, 1: 안읽음
    is_read = models.BooleanField(null=False, blank=False, default=1)
    # 0: 삭제
    status = models.BooleanField(default=1, null=False, blank=False)
    #     1. 모임 홍보글 댓글 알림
    #     2. 활동 상세글 댓글 알림
    #     3. 위시리스트 댓글 알림
    #     4. 쪽지 알림
    #     5. 틴친 신청 알림
    #     6. 모임 활동 개설 알림
    #     7. 모임 공지사항 알림
    #     8. 모임 틴플레이 알림
    #     9. 모임 가입 알림
    #     10. 모임 탈퇴 알림
    #     11. 활동 참가신청 관련 알림
    #     12. 활동 참가승인 알림
    #     13. 활동 참가거절 알림
    #     14. 틴친 승인 알림
    #     15. 틴친 거절 알림
    alarm_type = models.IntegerField(null=False, blank=False)
    sender = models.ForeignKey(Member, related_name='sender', null=False, blank=False, on_delete=models.PROTECT)
    receiver = models.ForeignKey(Member, related_name='receiver', null=False, blank=False, on_delete=models.PROTECT)

    objects = models.Manager()
    enabled_objects = AlarmManager()

    class Meta:
        db_table = 'tbl_alarm'
