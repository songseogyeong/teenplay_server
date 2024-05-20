from django.db import models


class RecentSearchManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True).order_by('-id')