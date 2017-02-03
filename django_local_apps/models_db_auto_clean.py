from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.models import TimeStampedModel


class DbCleanConfig(TimeStampedModel):
    content_type = models.ForeignKey(ContentType)
    expire_days = models.IntegerField()

