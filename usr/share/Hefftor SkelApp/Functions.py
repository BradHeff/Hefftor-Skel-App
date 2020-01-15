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
    md.format_secondary_markup(message)
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

# ===========================================
#		BACKUP BEFORE SKEL FUNCTION
# ===========================================


def processing(self, active_text):
    now = datetime.datetime.now()
    if self.firstrun == 0:

        GLib.idle_add(setProgress, self, 0.1)

        # ============================
        #       CONFIG
        # ============================

        copytree(self, home + '/.config', home + '/' + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + '/.config_backup-' +
                 now.strftime("%Y-%m-%d %H:%M:%S"))
        GLib.idle_add(setProgress, self, 0.3)

        # ============================
        #       LOACAL
        # ============================

        copytree(self, home + '/.local', home + '/' + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + '/.local_backup-' +
                 now.strftime("%Y-%m-%d %H:%M:%S"))
        GLib.idle_add(setProgress, self, 0.5)

        # ============================
        #       BASH
        # ============================
        shutil.copy(
            home + '/.bashrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.bashrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))

        # ============================
        #       CONKY
        # ============================
        copytree(self, home + '/.lua', home + '/' + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + '/.lua_backup-' +
                 now.strftime("%Y-%m-%d %H:%M:%S"))
        shutil.copy(
            home + '/.conkyrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.conkyrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))

        self.firstrun = 1
        GLib.idle_add(setMessage, self, "Done")

    GLib.idle_add(setMessage, self, "Running Skel")
    GLib.idle_add(setProgress, self, 0.8)
    GLib.idle_add(self.run, active_text)
    GLib.idle_add(self.refresh)
