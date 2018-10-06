from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TS_WHUT.settings')
django.setup()

app = Celery('TS_WHUT')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每天3点半执行一次
    sender.add_periodic_task(
        crontab(hour=3, minute=30),
        del_over_7_day_log.s(),
    )


@app.task
def del_over_7_day_log():
    from images.models import ImageModel
    from datetime import datetime
    from datetime import timedelta

    end_time = datetime.now() - timedelta(days=7)
    first_day = datetime(2018, 1, 1, 0, 0, 0)
    time_range = (first_day, end_time)

    images = ImageModel.objects.filter(if_active=4, add_time__range=time_range)
    for image in images:
        image.delete()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
