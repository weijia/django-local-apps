import datetime
import os

from django.utils import timezone
from tzlocal import get_localzone

from obj_sys import obj_tools
from obj_sys.models_ufs_obj import UfsObj
from tagging.models import Tag


class ObjectIsNotAssigned(Exception):
    pass


class UfsObjSaverBase(object):
    def __init__(self, user):
        super(UfsObjSaverBase, self).__init__()
        self.user = user
        self.source = UfsObj.SOURCE_WEB_POST
        self.last_modified = None
        self.parent = None
        self.create_param = None
        self.obj = None
        self.ufs_url = None
        self.full_path = None
        self.tag_app = None

    def filter_or_create(self):
        obj_filter = self.get_filter()
        if not obj_filter.exists():
            self.obj, is_created = self.get_or_create()
        else:
            self.obj = obj_filter[0]
        return obj_filter

    def get_or_create(self):
        obj_filter = self.get_filter()
        if obj_filter.exists():
            self.obj = obj_filter[0]
            return self.obj, False
        self.create_param = ({"ufs_url": self.ufs_url, "parent": self.parent, "user": self.user,
                              "full_path": self.full_path, "ufs_obj_type": self.ufs_obj_type,
                              "source": self.source})
        if not (self.last_modified is None):
            self.create_param["last_modified"] = self.last_modified
        self.obj, is_created = UfsObj.objects.get_or_create(**self.create_param)
        return self.obj, is_created

    def append_tags(self, tag_name):
        if self.obj is None:
            raise ObjectIsNotAssigned
        Tag.objects.add_tag(self.obj, tag_name, tag_app=self.tag_app)

    def add_description(self, description):
        self.obj.descriptions.add(description)
        # self.obj.save()


class UfsLocalObjSaver(UfsObjSaverBase):
    def __init__(self, user, ufs_obj_type=UfsObj.TYPE_UFS_OBJ):
        super(UfsLocalObjSaver, self).__init__(user)
        self.ufs_obj_type = ufs_obj_type

    def init_with_qt_url(self, qt_file_url):
        self.init_with_full_path(obj_tools.get_full_path_for_local_os(qt_file_url))

    def init_with_full_path(self, full_path):
        self.full_path = full_path
        self.ufs_url = obj_tools.get_ufs_url_for_local_path(self.full_path)
        tz = get_localzone()
        self.last_modified = tz.localize(datetime.datetime.fromtimestamp(os.path.getmtime(self.full_path)))

    def get_filter(self):
        return UfsObj.objects.filter(full_path=self.full_path, user=self.user)

    def get_or_create(self):
        obj, is_created = super(UfsLocalObjSaver, self).get_or_create()
        if os.path.isdir(self.full_path):
            self.__append_folder_tag()
        return obj, is_created

    def __append_folder_tag(self):
        self.append_tags("folder")

    def update_from_local_path(self):
        self.get_filter().update(last_modified=self.last_modified)

    @staticmethod
    def get_full_path_from_qt_url(url):
        return url.replace("file:///", "")

    @staticmethod
    def get_qt_url_from_full_path(full_path):
        return "file:///%s" % full_path


class UfsUrlObj(UfsObjSaverBase):
    def __init__(self, web_url, user, ufs_obj_type=UfsObj.TYPE_UFS_OBJ):
        super(UfsUrlObj, self).__init__(user)
        self.full_path = None
        self.ufs_url = web_url
        self.ufs_obj_type = ufs_obj_type

    def get_filter(self):
        return UfsObj.objects.filter(ufs_url=self.ufs_url, user=self.user)
