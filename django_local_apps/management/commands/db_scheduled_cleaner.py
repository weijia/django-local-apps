import logging


from pinax.eventlog.models import Log

from django_local_apps.management.commands.local_app_utils.db_clean_utils import remove_expired_record
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class DbScheduledCleaner(DjangoCmdBase):
    expire_days = 1
    models = [Log]
    query_set = None

    def msg_loop(self):
        expire_days = self.expire_days
        query_set = self.query_set
        if query_set is None:
            for model in self.models:
                query_set = model.objects
                remove_expired_record(expire_days, query_set)
        else:
            remove_expired_record(expire_days, query_set)


Command = DbScheduledCleaner
