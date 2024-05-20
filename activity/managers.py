from django.db import models


class ActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class ActivityImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class ActivityLikeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class ActivityMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class ActivityReplyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)