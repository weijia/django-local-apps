# -*- coding: utf-8 -*-
from django.db import models
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
