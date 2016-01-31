from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from obj_sys.models_ufs_obj import UfsObj
from obj_sys.ufs_obj_in_tree_view import ItemTreeView

urlpatterns = patterns('',
    url(r'^remove_tags_from/$', 'django_local_apps.views_obj_sys_local.remove_tags_from'),
    # url(r'^mmenu/$', TemplateView.as_view(template_name="django_local_apps/mmenu_base.html")),
    url(r'^tree/$', ItemTreeView.as_view(item_class=UfsObj,
                                         ufs_obj_type=UfsObj.TYPE_UFS_OBJ,
                                         default_level=1,
                                         template_name="django_local_apps/mmenu_base.html")),
    # url(r'^remove_thumb_for_paths/$', 'obj_sys.obj_tagging.remove_thumb_for_paths'),
    # url(r'^rm_objs_for_path/$', 'obj_sys.obj_tagging.rm_objs_for_path'),
    # url(r'^rm_obj_from_db/$', 'obj_sys.obj_tagging.rm_obj_from_db'),
    # url(r'^apply_tags_to/$', 'obj_sys.views.apply_tags_to'),
)
