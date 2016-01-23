

import pysftp

with pysftp.Connection('192.168.8.1', username='root', password='843ea28d5f') as sftp:
    print sftp.pwd
    with sftp.cd("/tmp/mnt/mmcblk0p1/"):
        print sftp.pwd
        for i in sftp.listdir_attr():
            print unicode(i)
    # with sftp.cd('public'):              # temporarily chdir to public
    #     sftp.put('/my/local/filename')  # upload file to public/ on remote
    #
    # sftp.get_r('myfiles', '/backup')    # recursively copy myfiles/ to local
