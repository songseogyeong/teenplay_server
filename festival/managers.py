from django.db import models


class FestivalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)