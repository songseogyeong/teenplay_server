from django.db import models
from django.utils import timezone


class Period(models.Model):
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        # 추상 모델을 설정(migrate 시 해당 모델의 테이블 생성X)
        abstract = True