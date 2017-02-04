import logging
import os

import sys
from optparse import make_option

from pinax.eventlog.models import Log

from django_local_apps.management.commands.local_app_utils.db_clean_utils import remove_expired_record
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class LocalCommandRunner(DjangoCmdBase):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('path', nargs='+')

    def msg_loop(self):
        print self.options["path"]


Command = LocalCommandRunner
