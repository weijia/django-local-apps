from djangoautoconf.local_key_manager import get_local_key

__author__ = 'weijia'


def get_ufs_web_server_port():
    return 8110


def get_admin_username():
    return get_local_key("admin_account.admin_username", "webmanager")


def get_admin_password():
    return get_local_key("admin_account.admin_password", "webmanager")
