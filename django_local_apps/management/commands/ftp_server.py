from django.core.management import BaseCommand
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.filesystems import AbstractedFS
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

__author__ = 'weijia'

# ref: https://groups.google.com/forum/#!topic/pyftpdlib/buePrncaNT4
class YourFS(AbstractedFS):
    def open(self, filename, mode):
        # do_db_stuff()
        return AbstractedFS.open(self, filename, mode)

    def mkstemp(self, suffix='', prefix='', dir=None, mode='wb'):
        # do_db_stuff()
        return AbstractedFS.mkstemp(self, file, "tmpfile")

    def listdir(self, path):
        # do_db_stuff()
        return AbstractedFS.listdir(self, path)


class FtpServer(BaseCommand):
    def handle(self, *args, **options):
        authorizer = DummyAuthorizer()
        authorizer.add_user('user', '12345', '.', perm='elradfmw')
        ftp_handler = FTPHandler
        ftp_handler.authorizer = authorizer
        ftp_handler.abstracted_fs = YourFS
        ftpd = FTPServer(('', 21), ftp_handler)
        ftpd.serve_forever()


Command = FtpServer