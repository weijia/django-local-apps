import os
from django_local_apps.management.commands.local_app_utils.filter_handler_base import FilterHandlerBase
from django_local_apps.management.commands.local_app_utils.local_app_counter import Counter
from django_local_apps.ufs_local_obj import UfsLocalObjSaver
from ufs_tools import format_path
from obj_sys.models_ufs_obj import UfsObj
from tagging.models import TaggedItem


class FolderIndexer(FilterHandlerBase):
    """
    Only process folders without PROCESSOR_ID: folder_indexer
    Updated folder will be checked by update checker. And update checker will remove the folder_indexer PROCESSOR_ID
    so folder indexer can check it again.
    """
    PROCESS_ID = "folder_indexer"

    def __init__(self):
        super(FolderIndexer, self).__init__()
        self.ignored_name_list = [".git", ".kuaipan", ".aptoide", "mini_mapv3", "emesene", "msi-b75", "Keil",
                                  "MicroMsg"]

    def get_obj_filter(self):
        ufs_obj_filter = TaggedItem.objects.get_by_model(
            UfsObj.objects.filter(ufs_obj_type=UfsObj.TYPE_UFS_OBJ, valid=True).exclude(
                indexedtime__local_index_type=self.process_id), ["folder",])
        return ufs_obj_filter

    def process_file(self, full_path, obj):
        print "processing: %s" % full_path

        if not (full_path is None) and (os.path.isdir(full_path)) and not self.is_ignore_container(obj):
            self.check_children(obj)
            folder_list = os.listdir(full_path)
            children_process_counter = Counter(len(folder_list), name="Children processing")
            # The following is required. otherwise, the tree will not be displayed correctly.
            with UfsObj.objects.delay_mptt_updates():
                for filename in folder_list:
                    if not self.is_ignore(filename):
                        child_full_path = format_path(os.path.join(full_path, filename))
                        if os.path.isdir(child_full_path):
                            self.create_or_update_obj(child_full_path, obj)
                    children_process_counter.increase()
        self.set_complete(obj)

    def create_or_update_obj(self, child_full_path, obj):
        # print unicode(child_full_path)
        obj_saver = UfsLocalObjSaver(self.admin_user)
        obj_saver.init_with_full_path(child_full_path)
        obj_saver.parent = obj
        obj_saver.source = UfsObj.SOURCE_INDEXER
        obj_saver.tag_app = self.PROCESS_ID
        if obj_saver.get_filter().exists():
            obj_saver.update_from_local_path()
        else:
            obj_saver.get_or_create()

    # noinspection PyMethodMayBeStatic
    def check_children(self, obj):
        children = UfsObj.objects.filter(parent=obj, valid=True)
        removed = []
        for child in children:
            if not os.path.exists(child.full_path):
                child.set_removed()
                child.save()

    # noinspection PyMethodMayBeStatic
    def is_ignore(self, filename):
        if filename == ".git":
            return True
        else:
            return False

    # noinspection PyMethodMayBeStatic
    def is_ignore_container(self, obj):
        is_ignored = False
        for ignore in self.ignored_name_list:
            if ignore in obj.full_path:
                is_ignored = True
        if "git" in obj.tags:
            is_ignored = True
        return is_ignored


Command = FolderIndexer
