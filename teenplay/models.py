import math
import datetime

from django.db import models

from club.models import Club
from member.models import Member
from teenplay.managers import TeenplayManager
from teenplay_server.models import Period, Like


class TeenPlay(Period):
    teenplay_title = models.TextField(null=False, blank=False)
    club = models.ForeignKey(Club, null=False, blank=False, on_delete=models.PROTECT)
    video_path = models.ImageField(upload_to='teenplay_video/%Y/%m/%d')
    thumbnail_path = models.ImageField(upload_to='teenplay_thumbnail/%Y/%m/%d')
    # 0: 삭제, 1: 게시중
    status = models.BooleanField(default=1, null=False, blank=False)
    objects = models.Manager()
    enable_objects = TeenplayManager()

    class Meta:
        db_table = 'tbl_teenplay'


class TeenPlayLike(Like):
    teenplay = models.ForeignKey(TeenPlay, null=False, blank=False, on_delete=models.PROTECT)
    # 0: 삭제, 1: 좋아요

    class Meta:
        db_table = 'tbl_teenplay_like'

    def change_date_format(self):
        now = datetime.datetime.now()
        create_date = self.created_date
        gap = math.floor((now - create_date).seconds / 60)

        if gap < 1:
            return "방금 전"

        if gap < 60:
            return f"{gap}분 전"

        gap = math.floor(gap / 60)

        if gap < 24:
            return f"{gap}시간 전"

        gap = math.floor(gap / 24)

        if gap < 31:
            return f"{gap}일 전"

        gap = math.floor(gap / 31)

        if gap < 12:
            return f"{gap}개월 전"

        gap = math.floor(gap / 12)
        return f"{gap}년 전"


