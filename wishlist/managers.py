from django.db import models


class WishlistManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)
    