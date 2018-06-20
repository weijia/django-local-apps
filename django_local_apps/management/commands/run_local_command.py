import logging
import os

import sys
from optparse import make_option
from subprocess import call

from pinax.eventlog.models import Log

from django_local_apps.management.commands.local_app_utils.db_clean_utils import remove_expired_record
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class LocalCommandRunner(DjangoCmdBase):

    def add_arguments(self, parser):
        # Positional arguments
        """
        :param: in the args it could be: /usr/local/bin/python /home/richard/codes/django-dev-server/manage.py help
        NO need to add '"' as "/usr/local/bin/python /home/richard/codes/django-dev-server/manage.py help"
        :return:
        """
        parser.add_argument('path', nargs='+')

    def msg_loop(self):
        print self.options["path"]
        call(self.options["path"])


Command = LocalCommandRunner
