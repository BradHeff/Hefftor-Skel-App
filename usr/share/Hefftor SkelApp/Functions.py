import Hefftor_SkelApp
from Hefftor_SkelApp import *


def setMessage(self, message):
    self.label4.set_text(message)


def setProgress(self, value):
    self.progressbar.set_fraction(value)


# ===========================================
#		DELETE BACKUP FUNCTION
# ===========================================
def Delete_Backup(self):
    
    for filename in os.listdir(home + "/" + bd):
        if filename == self.backs.get_active_text():
            shutil.rmtree(home + "/" + bd + "/" + filename)
    GLib.idle_add(refresh, self)
    GLib.idle_add(Functions.callBox,self, "Config backups cleaned.", "Success!!")
    GLib.idle_add(self.button_toggles, True)

# ===========================================
#		FLUSH ALL FUNCTION
# ===========================================
def Flush_All(self):
    count = os.listdir(home + "/" + bd).__len__()
    count = ((count/count)/count)

    for filename in os.listdir(home + "/" + bd):                
        if os.path.isdir(home + "/" + bd + "/" + filename):
            GLib.idle_add(setProgress, self, self.progressbar.get_fraction() + count)
            shutil.rmtree(home + "/" + bd + "/" + filename)            
            

    GLib.idle_add(refresh, self)
    GLib.idle_add(callBox,self, ".SkelApp_Backups directory has been cleaned.", "Success!!")
    GLib.idle_add(setProgress, self, 0)
    GLib.idle_add(self.button_toggles, True)

# ===========================================
#		REFRESH FUNCTION
# ===========================================
def refresh(self):
    if not os.path.exists(home + "/" + bd):
        os.makedirs(home + "/" + bd)

    self.backs.get_model().clear()
    BACKUPS_CATS = []
    for filename in os.listdir(home + "/" + bd):
        if os.path.isdir(home + "/" + bd + "/" + filename):
            BACKUPS_CATS.append(filename)
    print(BACKUPS_CATS)
    for item in BACKUPS_CATS:
        self.backs.append_text(item)

    self.backs.set_active(0)

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
    GLib.idle_add(run, self, active_text)
    GLib.idle_add(refresh, self)


# ===========================================
#		SKEL FUNCTION
# ===========================================
def run(self, cat):

    # ===========================================
    #		POLYBAR
    # ===========================================
    if cat == "polybar Configs":
        self.ecode = 0
        src = '/etc/skel/.config/polybar/'
        if not os.path.exists(src):
            self.ecode = 1
        else:
            copytree(self, src,
                                home + '/.config/polybar/')
            print("Path copied")

        print(self.ecode)
    
    # ===========================================
    #		HERBSTLUFTWM
    # ===========================================
    elif cat == "herbstluftwm Configs":
        self.ecode = 0
        src = '/etc/skel/.config/herbstluftwm/'
        if not os.path.exists(src):
            self.ecode = 1
            print(self.ecode)
        else:
            copytree(self, src, home + '/.config/herbstluftwm/',
                                )
            print("Path copied")

    # ===========================================
    #		BSPWM
    # ===========================================
    elif cat == "bspwm Configs":
        self.ecode = 0
        src = '/etc/skel/.config/bspwm/'
        if not os.path.exists(src):
            self.ecode = 1
        else:
            copytree(self, src, home + '/.config/bspwm/'
                                )
            print("Path copied")

    # ===========================================
    #		Betterlockscreen
    # ===========================================
    elif cat == "betterlockscreen cache":
        self.ecode = 0
        src1 = '/etc/skel/.cache/i3lock'

        if not os.path.exists(src1):
            self.ecode = 1
        else:
            copytree(self, src1, home + '/.cache/i3lock')

    # ===========================================
    #		ROOT
    # ===========================================
    elif cat == "root Configs":
        self.ecode = 0
        src1 = '/etc/skel/'

        if not os.path.exists(src1):
            self.ecode = 1
        else:
            for filename in os.listdir(src1):
                if os.path.isfile(src1 + filename):
                    print(filename)
                    shutil.copy(src1 + filename,
                                home + "/" + filename)

        print("Root Configs copied")

    # ===========================================
    #		LOCALS
    # ===========================================
    elif cat == "Local Configs":
        self.ecode = 0
        src1 = '/etc/skel/.local/bin'
        src2 = '/etc/skel/.local/share'
        
        if not os.path.exists(src1) or not os.path.exists(src2):
            self.ecode = 1
        else:
            for filename in os.listdir(src1):
                shutil.copy(src1 + "/" + filename, home + '/.local/bin/' + filename)
            
            for filename in os.listdir(src2):
                if os.path.exists(src2 + "/" + filename) and filename != "xfce4":
                    print(filename)
                    copytree(self, src2 + "/" + filename, home + '/.local/share/' + filename)

        print(".local copied")
    
    # ===========================================
    #		CONKY
    # ===========================================
    elif cat == "Conky Configs":
        self.ecode = 0
        src1 = '/etc/skel/.lua'
        src2 = '/etc/skel/.conkyrc'
        if not os.path.exists(src1) or not os.path.isfile(src2):
            self.ecode = 1
        else:
            copytree(self, src1, home + '/.lua')
            shutil.copy(src2, home + '/.conkyrc')

        print("Conky copied")

    # ===========================================
    #		DCONF
    # ===========================================
    elif cat == "dconf Configs":
        self.ecode = 0
        src1 = '/etc/skel/.config/dconf'
        if not os.path.exists(src1):
            self.ecode = 1
        else:
            copytree(self, src1, home + '/.config/dconf'
                                )

        print(".local copied")

    # ===========================================
    #		XFCE
    # ===========================================
    elif cat == "xfce Configs":
        self.ecode = 0
        src1 = '/etc/skel/.config/xfce4'
        src4 = '/etc/skel/.config/Thunar'
        src8 = '/etc/skel/.config/autostart'

        if not os.path.exists(src1):
            self.ecode = 1
        else:
            for folder in os.listdir(src1):
                if os.path.isdir(src1 + "/" + folder):
                    copytree(
                        self, src1 + "/" + folder, home + '/.config/xfce4/' + folder)
                elif os.path.isfile(src1 + "/" + folder):
                    shutil.copy(src1 + "/" + folder,
                                home + "/.config/xfce4/" + folder)

        if not os.path.exists(src4):
            self.ecode = 1
        else:
            for filename in os.listdir(src4):
                if os.path.isfile(src4 + "/" + filename):
                    shutil.copy(src4 + "/" + filename,
                                home + "/.config/Thunar/" + filename)

        if not os.path.exists(src8):
            self.ecode = 1
        else:
            for filename in os.listdir(src8):
                if os.path.isfile(src8 + "/" + filename):
                    shutil.copy(src8 + "/" + filename, home + "/.config/autostart/" + filename
                                )

        print("xfce copied")

    # ===========================================
    #		XFCE_CONFIGS PACKAGE
    # ===========================================
    elif cat == "xfce-config package":
        self.ecode = 0
        list = ["fontconfig","galculator","gtk-3.0","htop","nano","nomacs","qt5ct", "rofi", "volumeicon","mimeapps.list","Trolltech.conf","yad.conf"]
        for item in list:                
            if os.path.isdir("/etc/skel/.config/" + item):
                copytree(
                    self, "/etc/skel/.config/" + item, home + '/.config/' + item)

            if os.path.isfile("/etc/skel/.config/" + item):
                shutil.copy("/etc/skel/.config/" + item, home + "/.config/" + item)

        print("xfce copied")

    # ===========================================
    #		HLWM/BSPWM CONFIGS PACKAGE
    # ===========================================
    elif cat == "hlwm/bspwm configs package":
        self.ecode = 0
        src1 = '/etc/skel/.config/herbstluftwm/'
        src2 = '/etc/skel/.config/bspwm/'
        if not os.path.exists(src1) or not os.path.exists(src2):
            print("DOES NOT EXIST")
            self.ecode = 1
        else:
            list = ["dunst","fontconfig","galculator","gtk-3.0","htop","nano","nomacs","qt5ct","ranger","rofi","volumeicon","mimeapps.list","Trolltech.conf","yad.conf"]
            for item in list:                
                if os.path.isdir("/etc/skel/.config/" + item):
                    copytree(
                        self, "/etc/skel/.config/" + item, home + '/.config/' + item)

                if os.path.isfile("/etc/skel/.config/" + item):
                    shutil.copy("/etc/skel/.config/" + item, home + "/.config/" + item)

            print("hlwm-config copied")

    setProgress(self,1)
    if(self.ecode == 1):
        callBox(self, "Cant seem to find that source. Have you got it installed?", "Success!!")
    else:
        callBox(self, "Skel executed successfully.", "Success!!")

    setProgress(self,0)
    self.button_toggles(True)
    setMessage(self, "Idle...")