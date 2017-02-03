from django.utils import timezone


def remove_expired_record(expire_days, query_set):
    query_set.filter(timestamp__lt=timezone.now() - timezone.timedelta(days=expire_days)).delete()

