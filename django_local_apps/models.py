# -*- coding: utf-8 -*-
from django.db import models

from obj_sys.models_ufs_obj import UfsObj


class IndexedTime(models.Model):
    ufs_obj = models.ForeignKey(UfsObj)
    created = models.DateTimeField(auto_now_add=True)
