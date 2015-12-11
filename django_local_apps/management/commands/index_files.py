import os
import datetime
from django.contrib.auth.models import User
from tzlocal import get_localzone
from django_local_apps.models import IndexedTime, IndexType
from django_local_apps.server_configurations import get_admin_username
from libtool import format_path
from obj_sys.models_ufs_obj import UfsObj
from obj_sys.obj_tools import get_ufs_url_for_local_path
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase


class Counter(object):
    def __init__(self, total_number, interval=100, name="Counter"):
        super(Counter, self).__init__()
        self.total_number = total_number
        self.processed_child = 1
        self.interval = interval
        self.name = name
        print "%s total: %d" % (self.name, self.total_number)

    def increase(self):
        self.processed_child += 1
        if self.processed_child % self.interval == 0:
            print "%s processed: %d/%d" % (self.name, self.processed_child, self.total_number)


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
            ufs_obj_filter = self.get_obj_for_first_indexing()

    def do_first_index_for_obj_list(self, ufs_obj_filter):
        counter = Counter(ufs_obj_filter.count(), 1000, name="Object processing")
        for obj in ufs_obj_filter:
            # if IndexedTime.objects.filter(ufs_obj=obj, local_index_type=self.first_index_type).exists():
            #     raise "Nonono"
            self.process_filtered_object(obj)
            counter.increase()
            self.set_complete(obj)

    def process_filtered_object(self, obj):
        full_path = format_path(obj.full_path)
        print "processing: %s" % full_path

        # if os.path.isdir(full_path):
        #     obj.is_container = True
        # else:
        #     obj.is_container = False
        # obj.save()
        # processed += 1
        # if processed%1000 == 0:
        #     print "processed: %d/%d" % (processed, total_num)
        # continue
        # print u"processing: " + unicode(full_path)
        if not (full_path is None) and (os.path.isdir(full_path)):
            if self.is_ignore_container(obj):
                return
            dir_list = os.listdir(full_path)
            children_process_counter = Counter(len(dir_list), name="Children processing")
            for filename in dir_list:
                if not self.is_ignore(filename):
                    child_full_path = format_path(os.path.join(full_path, filename))
                    # print unicode(child_full_path)
                    new_obj = self.add_obj_from_full_path(child_full_path, obj)
                    if not os.path.isdir(child_full_path):
                        self.set_complete(new_obj)
                    children_process_counter.increase()

    def set_complete(self, new_obj):
        IndexedTime.objects.get_or_create(ufs_obj=new_obj, local_index_type=self.first_index_type)

    def get_obj_for_first_indexing(self):
        ufs_obj_filter = UfsObj.objects.filter(ufs_obj_type=UfsObj.TYPE_UFS_OBJ, is_container=True). \
            exclude(indexedtime__local_index_type=self.first_index_type)
        return ufs_obj_filter

    def add_obj_from_full_path(self, child_full_path, parent_obj):
        file_url = get_ufs_url_for_local_path(child_full_path)
        is_container = os.path.isdir(child_full_path)
        tz = get_localzone()
        last_modified_with_timezone = tz.localize(datetime.datetime.fromtimestamp(os.path.getmtime(child_full_path)))

        existing_obj = UfsObj.objects.filter(full_path=child_full_path)
        if existing_obj.exists():
            obj = existing_obj[0]
            is_updated = False
            if obj.is_container != is_container:
                obj.is_container = is_container
                is_updated = True
            modified_diff = obj.last_modified - last_modified_with_timezone
            if modified_diff.days > 1:
                is_updated = True
            if is_updated:
                obj.save()
        else:
            obj, is_created = UfsObj.objects.get_or_create(
                ufs_obj_type=UfsObj.TYPE_UFS_OBJ, ufs_url=file_url,
                parent=parent_obj, is_container=is_container,
                full_path=child_full_path, user=self.admin_user,
                source=UfsObj.SOURCE_INDEXER,
                last_modified=last_modified_with_timezone,
            )
        return obj

    def is_ignore(self, filename):
        if filename == ".git":
            return True
        else:
            return False

    # noinspection PyMethodMayBeStatic
    def is_ignore_container(self, obj):
        if "git" in obj.tags:
            return True
        else:
            return False


Command = NoMsgHandler
