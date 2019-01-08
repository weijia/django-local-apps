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
        # for using with chronograph, do not use nargs param, because chronograph seems do not support passing
        # array, but using nargs will generate a list for the parameters
        parser.add_argument('-c', '--container_id')
        parser.add_argument('-w', '--work_dir', default=None)
        parser.add_argument('path_and_params', nargs='+')

    def msg_loop(self):
        print(self.options["container_id"])
        print(self.options["work_dir"])
        print(self.options["path_and_params"])
        client = docker.from_env(timeout=3600)
        container = client.containers.get(self.options["container_id"])
        print(container.exec_run(" ".join(self.options["path_and_params"]), workdir=(self.options["work_dir"])))


Command = DockerExecutor
