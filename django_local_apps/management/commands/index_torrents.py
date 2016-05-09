import json
from torrentool.torrent import Torrent
from django_local_apps.management.commands.local_app_utils.filter_handler_base import FilterHandlerBase
from django_local_apps.management.commands.local_app_utils.local_app_counter import Counter
from django_local_apps.models import IndexedTime, IndexType
from ufs_tools import format_path
from obj_sys.models_ufs_obj import UfsObj


class TorrentIndexer(FilterHandlerBase):
    PROCESS_ID = "torrent_indexer"

    def get_obj_filter(self):
        ufs_obj_filter = UfsObj.objects.filter(ufs_obj_type=UfsObj.TYPE_UFS_OBJ, full_path__icontains=".torrent"). \
            exclude(indexedtime__local_index_type=self.process_id)
        return ufs_obj_filter

    def process_file(self, full_path, obj):
        try:
            torrent = Torrent.from_file(full_path)
            for torrent_file in torrent.files:
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
        except:
            pass

Command = TorrentIndexer
