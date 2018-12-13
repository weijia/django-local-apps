import logging
import docker
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class DockerExecutor(DjangoCmdBase):

    def add_arguments(self, parser):
        # Positional arguments
        """
        :param: in the args it could be: /usr/local/bin/python /home/richard/codes/django-dev-server/manage.py help
        NO need to add '"' as "/usr/local/bin/python /home/richard/codes/django-dev-server/manage.py help"
        :return:
        """
        parser.add_argument('container_id', nargs=1)
        parser.add_argument('work_dir', nargs='?', default=None)
        parser.add_argument('path_and_params', nargs='+')

    def msg_loop(self):
        print(self.options["path_and_params"])
        client = docker.from_env()
        container = client.containers.get(self.options["container_id"])
        container.exec_run(" ".join(self.options["path_and_params"]), workdir=self.options["work_dir"])


Command = DockerExecutor
