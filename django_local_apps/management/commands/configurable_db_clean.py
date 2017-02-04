import logging
from django_local_apps.management.commands.local_app_utils.db_clean_utils import remove_expired_record
from django_local_apps.models_db_auto_clean import DbCleanConfig
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase


log = logging.getLogger()


class ConfigurableDbCleaner(DjangoCmdBase):
    def msg_loop(self):
        for db_clean_config in DbCleanConfig.objects.all():
            query_set = db_clean_config.content_type.model_class().objects
            remove_expired_record(db_clean_config.expire_days, query_set)


Command = ConfigurableDbCleaner
