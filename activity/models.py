from django.db import models

from activity.managers import ActivityManager, ActivityImageManager, ActivityLikeManager, ActivityMemberManager, \
    ActivityReplyManager
from club.models import Club
from festival.models import Festival
from member.models import Member
from pay.models import Pay
from teenplay_server.category import Category
from teenplay_server.models import Like
from teenplay_server.period import Period


class Activity(Period):
    club = models.ForeignKey(Club, null=False, blank=False, on_delete=models.PROTECT)
    activity_title = models.TextField(null=False, blank=False)
    activity_content = models.TextField(null=False, blank=False)
    recruit_start = models.DateTimeField(null=False, blank=False)
    recruit_end = models.DateTimeField(null=False, blank=False)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.PROTECT)
    activity_intro = models.TextField(null=True)
    activity_address_location = models.TextField(null=True)
    activity_address_detail = models.TextField(null=True)
    thumbnail_path = models.ImageField(upload_to='activity/%Y/%m/%d')
    banner_path = models.ImageField(upload_to='activity/%Y/%m/%d')
    activity_start = models.DateTimeField(null=False, blank=False)
    activity_end = models.DateTimeField(null=False, blank=False)
    festival = models.ForeignKey(Festival, null=True, on_delete=models.PROTECT)
    pay = models.ForeignKey(Pay, null=False, blank=False, on_delete=models.PROTECT)
    # 0: 삭제, 1: 활동중
    status = models.BooleanField(default=1, null=False, blank=False)

    objects = models.Manager()
    enabled_objects = ActivityManager()

    class Meta:
        db_table = 'tbl_activity'

    def get_absolute_url(self):
        return f'/activity/detail/?id={self.id}'


class ActivityImage(Period):
    activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.PROTECT)
    image_path = models.ImageField(null=False, blank=False, upload_to='activity/%Y/%m/%d')

    # 0: 삭제
    status = models.BooleanField(default=1, null=False, blank=False)

    objects = models.Manager()
    enabled_objects = ActivityImageManager()

    class Meta:
        db_table = 'tbl_activity_image'


class ActivityLike(Like):
    activity = models.ForeignKey(Activity, null=False, blank=False, on_delete=models.PROTECT)
    # 0: 삭제, 1: 좋아요

    objects = models.Manager()
    enabled_objects = ActivityLikeManager()

    class Meta:
        db_table = 'tbl_activity_like'


class ActivityMember(Period):
    ACTIVITY_MEMBER_STATUS = [
        (-1, '참가대기'),
        (0, '취소'),
        (1, '참가중')
    ]

    member = models.ForeignKey(Member, null=False, blank=False, on_delete=models.PROTECT)
    activity = models.ForeignKey(Activity, null=False, blank=False, on_delete=models.PROTECT)
    # -1: 참가대기, 0: 취소, 1: 참가중
    status = models.SmallIntegerField(choices=ACTIVITY_MEMBER_STATUS, default=0, null=False, blank=False)

    objects = models.Manager()
    enabled_objects = ActivityMemberManager()

    class Meta:
        db_table = 'tbl_activity_member'


class ActivityReply(Period):
    activity = models.ForeignKey(Activity, null=False, blank=False, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, null=False, blank=False, on_delete=models.PROTECT)
    reply_content = models.TextField(null=False, blank=False)
    # 0: 삭제, 1: 게시중
    status = models.BooleanField(default=1, null=False, blank=False)

    objects = models.Manager()
    enabled_objects = ActivityReplyManager()

    class Meta:
        db_table = 'tbl_activity_reply'
