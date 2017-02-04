import logging
import os

import sys
from pinax.eventlog.models import Log

from django_local_apps.management.commands.local_app_utils.db_clean_utils import remove_expired_record
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class LocalCommandRunner(DjangoCmdBase):

    def msg_loop(self):
        print sys.argv
        os.system(sys.argv[2])


Command = LocalCommandRunner
