from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^remove_tags_from/$', 'django_local_apps.views_obj_sys_local.remove_tags_from'),
    # url(r'^remove_thumb_for_paths/$', 'obj_sys.obj_tagging.remove_thumb_for_paths'),
    # url(r'^rm_objs_for_path/$', 'obj_sys.obj_tagging.rm_objs_for_path'),
    # url(r'^rm_obj_from_db/$', 'obj_sys.obj_tagging.rm_obj_from_db'),
    # url(r'^apply_tags_to/$', 'obj_sys.views.apply_tags_to'),
)
