from django.db import models

from member.models import Member
from teenplay_server.period import Period


class Friend(Period):
    FRIEND_STATUS = [
        (-1, '대기중'),
        (0, '거절'),
        (1, '친구중')
    ]

    sender = models.ForeignKey(Member, related_name='friend_sender', null=False, blank=False, on_delete=models.PROTECT)
    receiver = models.ForeignKey(Member, related_name='friend_receiver', null=False, blank=False, on_delete=models.PROTECT)
    # -1: 대기중, 0: 거절, 1: 친구중
    is_friend = models.SmallIntegerField(null=False, blank=False, default=-1)

    class Meta:
        db_table = 'tbl_friend'
