# -*- coding: utf-8 -*-
from django.db import models
from ufs_tools.short_decorator.ignore_exception import ignore_exc

from django_local_apps.postgres_sql_checker import wait_for_postgres_sql
from djangoautoconf.auto_conf_signals import before_server_start, before_server_stop
from ufs_tools.direct_opener import open_url
from obj_sys.models_ufs_obj import UfsObj


class IndexType(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return unicode(self.name)


class IndexedTime(models.Model):
    ufs_obj = models.ForeignKey(UfsObj)
    created = models.DateTimeField(auto_now_add=True)
    local_index_type = models.ForeignKey(IndexType)

    def __unicode__(self):
        return unicode(self.ufs_obj) + u" "+ unicode(self.local_index_type) + "->" + unicode(self.created)


def start_callback(sender, **kwargs):
    print("Request started!")
    wait_for_postgres_sql()


before_server_start.connect(start_callback)


def stop_cherrypy():
    stop_main_server()


@ignore_exc
def stop_main_server():
    stop_url_base = 'http://localhost:%d/stop/quit'
    full_web_url = stop_url_base % 8110
    open_url(full_web_url)


# @ignore_exc
# def stop_thumb_server():
#     full_web_url = stop_url_base % configuration.g_config_dict["thumb_server_port"]
#     open_url(full_web_url)
#
#
# def stop_services_and_web_servers():
#     print "stopping services"
#     shutdown_all()
#     print "stopping web servers"
#     stop_main_server()
#     stop_thumb_server()

def end_callback(sender, **kwargs):
    print("Request ended!")
    stop_cherrypy()


before_server_stop.connect(end_callback)
