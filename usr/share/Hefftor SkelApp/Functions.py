# from distutils.dir_util import copy_tree, remove_tree
# from distutils.file_util import copy_file
from os.path import expanduser
import os
import shutil
home = expanduser("~")


class Functions(object):

    def copytree(self, src, dst, symlinks=False, ignore=None):

        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                except Exception as e:
                    print(e)
                    os.unlink(d)
            if os.path.isdir(s):
                try:
                    shutil.copytree(s, d, symlinks, ignore)
                except Exception as e:
                    print(e)
                    print("ERROR2")
                    ecode = 1
            else:
                try:
                    shutil.copy2(s, d)
                except:
                    print("ERROR3")
                    ecode = 1
