from django.db import models

from member.models import Member
from teenplay_server.period import Period


class Letter(Period):
    sender = models.ForeignKey(Member, null=False, blank=False, on_delete=models.PROTECT, related_name='letter_sender')
    receiver = models.ForeignKey(Member, null=False, blank=False, on_delete=models.PROTECT, related_name='letter_receiver')
    letter_content = models.TextField(null=False, blank=False)
    # 0: 삭제
    status = models.BooleanField(default=1, null=False, blank=False)

    class Meta:
        db_table = 'tbl_letter'
        ordering = ['-id']


class ReceivedLetter(Period):
    letter = models.ForeignKey(Letter, null=False, blank=False, on_delete=models.PROTECT)
    # 0: 읽음, 1: 안읽음
    is_read = models.BooleanField(null=False, blank=False, default=1)
    # 0: 삭제
    status = models.BooleanField(default=1, null=False, blank=False)

    class Meta:
        db_table = 'tbl_received_letter'


class SentLetter(Period):
    letter = models.ForeignKey(Letter, null=False, blank=False, on_delete=models.PROTECT)
    # 0: 삭제
    status = models.BooleanField(default=1, null=False, blank=False)

    class Meta:
        db_table = 'tbl_sent_letter'
