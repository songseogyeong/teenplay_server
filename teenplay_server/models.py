from django.db import models
from django.utils import timezone

from member.models import Member
from teenplay_server.period import Period


class Region(Period):
    region = models.TextField(null=False, blank=False)
    # 0: 삭제
    status = models.BooleanField(null=False, blank=False, default=1)

    class Meta:
        db_table = 'tbl_region'


class Like(Period):
    member = models.ForeignKey(Member, null=False, blank=False, on_delete=models.PROTECT)
    status = models.BooleanField(default=1, null=False, blank=False)

    class Meta:
        # 추상 모델을 설정(migrate 시 해당 모델의 테이블 생성X)
        abstract = True