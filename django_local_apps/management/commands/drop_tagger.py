from django_local_apps.server_configurations import get_ufs_web_server_port, get_admin_username, get_admin_password
from iconizer.gui_client.browser_service_client import BrowserServiceClass
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from libtool.string_tools import quote_unicode
from universal_clipboard.management.commands.cmd_handler_base.msg_process_cmd_base import MsgProcessCommandBase

__author__ = 'weijia'


class DropTagger(MsgProcessCommandBase):
    # noinspection PyMethodMayBeStatic
    def is_need_process(self, msg):
        if ("msg_type" in msg) and (msg["msg_type"] == "drop"):
            return True

    def process_msg(self, msg):
        if self.is_need_process(msg):
            if "urls" in msg:
                links = ""
                for i in msg["urls"]:
                    links += "url=" + quote_unicode(unicode(i)) + "&"
                tagging_url = "http://127.0.0.1:%s/webmanager/login_and_go_home/?" \
                         "username=%s&password=%s&target=" \
                         "/obj_sys/tagging_local/?%s" % (
                         str(get_ufs_web_server_port()), get_admin_username(), get_admin_password(), links)
                print tagging_url
                BrowserServiceClass().open_browser(tagging_url)

    def register_to_service(self):
        channel = self.get_channel("drop_target_channel")
        self.ufs_msg_service.send_to(
            ICONIZER_SERVICE_NAME,
            {"command": "DropWndV2", "tip": "Drop test", "target": channel.get_channel_full_name()})
        return channel


Command = DropTagger
