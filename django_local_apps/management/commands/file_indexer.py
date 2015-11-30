import os

from django_git.management.commands.git_pull_all import get_full_path_from_url
from django_local_apps.models import IndexedTime
from obj_sys.models_ufs_obj import UfsObj
from obj_sys.obj_tools import get_ufs_url_for_local_path
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase


class NoMsgHandler(MsgProcessCommandBase):
    def msg_loop(self):
        # super(NoMsgHandler, self).msg_loop()
        # for obj in UfsObj.objects.filter(ufs_obj_type=UfsObj.INDEXING_FILE):
        for obj in UfsObj.objects.filter(indexedtime__ufs_obj=None, ufs_obj_type=UfsObj.UFS_OBJ_TYPE):
            full_path = obj.full_path
            if not (full_path is None) and (os.path.isdir(full_path)):
                for filename in os.listdir(full_path):
                    file_url = get_ufs_url_for_local_path(os.path.join(full_path, filename))
                    UfsObj.objects.get_or_create(ufs_obj_type=UfsObj.INDEXING_FILE, ufs_url=file_url)
            IndexedTime.objects.get_or_create(ufs_obj=obj)


Command = NoMsgHandler
