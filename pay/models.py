from django.db import models

from member.models import Member
from teenplay_server.period import Period


class Pay(Period):
    member = models.ForeignKey(Member, null=False, blank=False, on_delete=models.PROTECT)
    price = models.IntegerField(default=20000, null=False, blank=False)
    receipt_id = models.TextField(null=True)
    # 0: 결제취소, 1: 결제완료
    status = models.BooleanField(default=1, null=False, blank=False)

    class Meta:
        db_table = 'tbl_pay'

class PayCancel(Period):
    pay_cancel_reason = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'tbl_pay_cancel'
