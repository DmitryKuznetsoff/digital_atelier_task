import datetime

from django.utils import timezone


def fix_naive_tz(naive_dt):
    current_tz = timezone.get_current_timezone()
    dt_obj = datetime.datetime.strptime(naive_dt, "%Y-%m-%d %H:%M:%S.%f")
    return current_tz.localize(dt_obj)
