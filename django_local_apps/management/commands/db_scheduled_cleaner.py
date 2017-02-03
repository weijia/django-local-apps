import logging

from django.utils import timezone
from pinax.eventlog.models import Log

from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class DbScheduledCleaner(DjangoCmdBase):
    expire_days = 1
    models = [Log]
    query_set = None

    def msg_loop(self):
        if self.query_set is None:
            for model in self.models:
                model.objects.filter(timestamp__lt=timezone.now()-timezone.timedelta(days=self.expire_days)).delete()
        else:
            self.query_set.filter(timestamp__lt=timezone.now()-timezone.timedelta(days=self.expire_days)).delete()


Command = DbScheduledCleaner
