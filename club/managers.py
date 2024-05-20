from django.db import models


class ClubManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class ClubMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class ClubPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class ClubPostReplyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)
