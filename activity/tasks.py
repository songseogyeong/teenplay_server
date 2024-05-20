import os
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule

from activity.models import ActivityImage


class DeleteOldImages(CronJobBase):
    RUN_EVERY_MIDNIGHT = Schedule(run_at_times=['00:00'])

    def do(self):
        delete_old_images()


def delete_old_images():
    yesterday = datetime.now() - timedelta(days=1)

    old_images = ActivityImage.objects.filter(status=0, created_date__lte=yesterday)

    for old_image in old_images:
        if old_image.image_path:
            image_path = old_image.image_path.path

            if os.path.exists(image_path):
                os.remove(image_path)
