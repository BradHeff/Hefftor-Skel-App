import Hefftor_SkelApp
from Hefftor_SkelApp import *


def setMessage(self, message):
    self.label4.set_text(message)


def setProgress(self, value):
    self.progressbar.set_fraction(value)

# ===========================================
#		MESSAGEBOX FUNCTION
# ===========================================


def callBox(self, message, title):
    message = message
    title = title

    md = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                           buttons=Gtk.ButtonsType.OK, text=title)
    md.format_secondary_text(message)
    md.run()
    md.destroy()
    # self.set_sensitive(True)

# ===========================================
#		SHUTIL COPY_TREE FUNCTION
# ===========================================


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
