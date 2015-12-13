import json

import time
from torrentool.torrent import Torrent

from django_local_apps.management.commands.local_app_utils.local_app_counter import Counter
from django_local_apps.models import IndexedTime, IndexType
from iconizer.msg_service.msg_service_interface.msg_service_provider_interface import InterfaceNotImplemented
from libtool import format_path
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase


# noinspection PyMethodMayBeStatic
class FilterHandlerBase(MsgProcessCommandBase):
    def __init__(self):
        super(FilterHandlerBase, self).__init__()
        self.process_id, is_created = IndexType.objects.get_or_create(name=self.PROCESS_ID)
        self.counter = None

    def msg_loop(self):
        while True:
            obj_filter = self.get_obj_filter()
            self.counter = Counter(obj_filter.count(), 10, name="Object processing")
            for obj in obj_filter:
                self.process_obj(obj)
            time.sleep(10)

    def get_obj_filter(self):
        raise InterfaceNotImplemented

    def process_obj(self, obj):
        full_path = format_path(obj.full_path)
        if not (full_path is None):
            self.process_file(full_path, obj)
        self.counter.increase()

    def set_complete(self, obj):
        IndexedTime.objects.get_or_create(ufs_obj=obj, local_index_type=self.process_id)

    def process_file(self, full_path, obj):
        raise InterfaceNotImplemented
