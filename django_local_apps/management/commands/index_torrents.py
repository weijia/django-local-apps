import json
import os
from django.contrib.auth.models import User
from torrentool.torrent import Torrent

from django_local_apps.models import IndexedTime, IndexType
from django_local_apps.server_configurations import get_admin_username
from libtool import format_path
from obj_sys.models_ufs_obj import UfsObj
from obj_sys.obj_tools import get_ufs_url_for_local_path
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase


class NoMsgHandler(MsgProcessCommandBase):
    PROCESS_ID = "torrent_indexer"

    def __init__(self):
        super(NoMsgHandler, self).__init__()
        self.process_id, is_created = IndexType.objects.get_or_create(name=self.PROCESS_ID)

    def msg_loop(self):
        for obj in self.get_obj_filter():
            self.process_obj(obj)

    def get_obj_filter(self):
        ufs_obj_filter = UfsObj.objects.filter(ufs_obj_type=UfsObj.TYPE_UFS_OBJ, full_path__icontains=".torrent"). \
            exclude(indexedtime__local_index_type=self.process_id)
        return ufs_obj_filter

    def process_obj(self, obj):
        full_path = format_path(obj.full_path)
        if not (full_path is None):
            self.process_file(full_path, obj)

    def set_complete(self, obj):
        IndexedTime.objects.get_or_create(ufs_obj=obj, local_index_type=self.process_id)

    def process_file(self, full_path, obj):
        torrent = Torrent.from_file(full_path)
        for torrent_file in torrent.files:
            if True:  # try:
                name = torrent_file[0]
                size = torrent_file[1]
                # file_storage_hash = file.storage_hash
                # file_modified = file.modified
                new_obj, is_created = UfsObj.objects.get_or_create(
                    ufs_obj_type=UfsObj.TYPE_UFS_OBJ,
                    ufs_url="ufs_torrent_content://%s" % name,
                    description_json=json.dumps({
                        # "storage_hash": file_storage_hash, "modified": file_modified
                        "name": name, "size": size,
                    }),
                    size=size,
                    parent=obj, user=self.admin_user,
                    source=UfsObj.SOURCE_INDEXER)
                self.set_complete(obj)
            else:  # except:
                pass

Command = NoMsgHandler
