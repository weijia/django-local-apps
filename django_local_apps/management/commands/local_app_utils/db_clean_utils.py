from django.db.models import Q
from django.utils import timezone


def remove_expired_record(expire_days, query_set, time_attr_name="timestamp"):
    expired_record_filter = {"%s__lt" % time_attr_name: timezone.now() - timezone.timedelta(days=expire_days)}
    q = Q(**expired_record_filter)
    final_q = query_set.filter(q)
    # cnt = 0
    # for i in final_q:
    #     i.delete()
    #     cnt += 1
    #     if cnt % 1000 == 0:
    #         print "%d deleted" % cnt
    final_q.delete()
