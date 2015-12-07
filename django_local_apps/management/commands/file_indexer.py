import os

from django.contrib.auth.models import User

from django_local_apps.models import IndexedTime, IndexType
from django_local_apps.server_configurations import get_admin_username
from obj_sys.models_ufs_obj import UfsObj
from obj_sys.obj_tools import get_ufs_url_for_local_path
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase


class NoMsgHandler(MsgProcessCommandBase):
    """
    Scan all files first and then retrieve detail of these files
    object state: indexing, indexed
    obj type: TYPE_UFS_OBJ
    indexed but detail not collected:
    indexed and detail collected:
    """
    FILE_INDEX_FIRST_STAGE_NAME = "first_index"
    FILE_INDEX_SECOND_STAGE_NAME = "second_index"

    def __init__(self):
        super(NoMsgHandler, self).__init__()
        # super(NoMsgHandler, self).msg_loop()
        # for obj in UfsObj.objects.filter(ufs_obj_type=UfsObj.INDEXING_FILE):
        self.first_index_type, is_created = IndexType.objects.get_or_create(name=self.FILE_INDEX_FIRST_STAGE_NAME)

    def msg_loop(self):
        self.do_first_index()

    def do_first_index(self):
        # The commented code will not work
        # for obj in UfsObj.objects.filter(indexedtime__ufs_obj=None,
        #                                  indexedtime__local_index_type=first_index_type,
        #                                  ufs_obj_type=UfsObj.TYPE_UFS_OBJ):
        # ufs_obj_filter = UfsObj.objects.filter(indexedtime__ufs_obj=None,
        #                                        ufs_obj_type=UfsObj.TYPE_UFS_OBJ).filter()
        ufs_obj_filter = self.get_obj_for_first_indexing()
        # query = ufs_obj_filter.query
        while ufs_obj_filter.count() > 0:
            self.do_first_index_for_obj_list(ufs_obj_filter)

    def do_first_index_for_obj_list(self, ufs_obj_filter):
        for obj in ufs_obj_filter:
            full_path = obj.full_path
            print u"processing: " + unicode(full_path)
            if not (full_path is None) and (os.path.isdir(full_path)):
                for filename in os.listdir(full_path):
                    child_full_path = os.path.join(full_path, filename)
                    self.add_obj_from_full_path(child_full_path)
            IndexedTime.objects.get_or_create(ufs_obj=obj, local_index_type=self.first_index_type)

    def get_obj_for_first_indexing(self):
        ufs_obj_filter = UfsObj.objects.exclude(indexedtime__local_index_type=self.first_index_type,
                                                ufs_obj_type=UfsObj.TYPE_UFS_OBJ)
        return ufs_obj_filter

    def add_obj_from_full_path(self, child_full_path):
        file_url = get_ufs_url_for_local_path(child_full_path)
        UfsObj.objects.get_or_create(ufs_obj_type=UfsObj.TYPE_UFS_OBJ, ufs_url=file_url,
                                     full_path=child_full_path, user=self.admin_user, source=UfsObj.SOURCE_INDEXER)


Command = NoMsgHandler
