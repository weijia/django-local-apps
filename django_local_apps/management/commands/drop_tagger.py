from UserDict import UserDict

from django_git.management.commands.git_pull_all import get_full_path_from_url
from django_local_apps.server_configurations import get_ufs_web_server_port, get_admin_username, get_admin_password
from iconizer.gui_client.browser_service_client import BrowserServiceClass
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from libtool.string_tools import quote_unicode
from obj_sys.obj_sys_client import ObjSysClint
from obj_sys.obj_tools import get_ufs_url_for_local_path
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
                    full_path = get_full_path_from_url(i)
                    ufs_url = get_ufs_url_for_local_path(full_path)
                    links += "url=" + quote_unicode(unicode(ufs_url)) + "&"
                c = ObjSysClint()
                c.password = get_admin_password()
                c.server_port = str(get_ufs_web_server_port())
                c.username = get_admin_username()
                tagging_url = c.get_manual_tagging_url(links)
                # print tagging_url
                BrowserServiceClass().open_browser(tagging_url)

    def register_to_service(self):
        channel = self.get_channel("drop_target_channel")
        reg_msg = UserDict({"command": "DropWndV2", "tip": "Tagging", "target": channel.get_channel_full_name()})
        self.ufs_msg_service.send_to(ICONIZER_SERVICE_NAME, reg_msg.data)
        return channel


Command = DropTagger
