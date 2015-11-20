from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
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
                print msg["urls"]
                # self.platform_service.open_browser()

    def register_to_service(self):
        channel = self.get_channel("drop_target_channel")
        self.ufs_msg_service.send_to(
            ICONIZER_SERVICE_NAME,
            {"command": "DropWndV2", "tip": "Drop test", "target": channel.get_channel_full_name()})
        return channel


Command = DropTagger
