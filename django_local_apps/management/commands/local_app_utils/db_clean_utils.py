from django.db.models import Q
from django.utils import timezone


def remove_expired_record(expire_days, query_set, time_attr_name="timestamp"):
    expired_record_filter = {"%s_lt" % time_attr_name: timezone.now() - timezone.timedelta(days=expire_days)}
    q = Q(**expired_record_filter)
    query_set.filter(q).delete()
