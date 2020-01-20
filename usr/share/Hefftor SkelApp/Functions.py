import os
import Hefftor_SkelApp
from Hefftor_SkelApp import home,bd,datetime,GLib,shutil,Gtk,re


def setMessage(self, message):
    self.label4.set_markup("<i>" + message + "</i>")


def setProgress(self, value):
    self.progressbar.set_fraction(value)


# ===========================================
#		UPGRADE ZSHRC FUNCTION
# ===========================================
def upgrade_zsh(self):
    now = datetime.datetime.now()
    GLib.idle_add(setMessage,self, "Running Backup")

    if not os.path.exists(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H")):
        os.makedirs(home + "/" + bd + "/Backup-" +
                    now.strftime("%Y-%m-%d %H"))

    if os.path.isfile(home + '/.zshrc'):
        shutil.copy(
            home + '/.zshrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.bashrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))
    
    if os.path.isfile("/etc/skel/.zshrc"):
        shutil.copy("/etc/skel/.zshrc", home + "/.zshrc")

        GLib.idle_add(setMessage,self, ".zshrc upgrade done")
        GLib.idle_add(callBox,self, "zshrc upgraded", "Success!!")
    else:
        GLib.idle_add(callBox,
            self, "zshrc upgrade failed, you dont have a .zshrc-latest in skel", "Failed!!")

    GLib.idle_add(setMessage,self, "Idle...")
    GLib.idle_add(refresh,self)
    GLib.idle_add(self.button_toggles,True)

# ===========================================
#		UPGRADE BASHRC FUNCTION
# ===========================================
def bash_upgrade(self):
    now = datetime.datetime.now()
    GLib.idle_add(setMessage,self, "Running Backup")

    if not os.path.exists(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H")):
        os.makedirs(home + "/" + bd + "/Backup-" +
                    now.strftime("%Y-%m-%d %H"))

    if os.path.isfile(home + '/.bashrc'):
        shutil.copy(
            home + '/.bashrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.bashrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))

    if os.path.isfile(home + '/.inputrc'):
        shutil.copy(
            home + '/.inputrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.inputrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))

    GLib.idle_add(setMessage,self, "Upgrading Bashrc")

    if os.path.isfile("/etc/skel/.inputrc-latest"):
        shutil.copy("/etc/skel/.inputrc-latest", home + "/.inputrc")
        shutil.copy("/etc/skel/.inputrc-latest",
                    home + "/.inputrc-latest")

    if os.path.isfile("/etc/skel/.bashrc-latest"):
        shutil.copy("/etc/skel/.bashrc-latest", home + "/.bashrc")
        shutil.copy("/etc/skel/.bashrc-latest", home + "/.bashrc-latest")

        GLib.idle_add(setMessage,self, ".bashrc upgrade done")
        GLib.idle_add(callBox,self, "bashrc upgraded", "Success!!")
    else:
        GLib.idle_add(callBox,
            self, "bashrc upgrade failed, you dont have a .bashrc-latest in skel", "Failed!!")

    GLib.idle_add(setMessage,self, "Idle...")
    GLib.idle_add(refresh,self)
    GLib.idle_add(self.button_toggles,True)

# ===========================================
#		DELETE BACKUP FUNCTION
# ===========================================
def Delete_Backup(self):
    count = os.listdir(home + "/" + bd).__len__()

    if count > 0:
        GLib.idle_add(setProgress, self, 0.3)
        for filename in os.listdir(home + "/" + bd):
            if filename == self.backs.get_active_text():
                shutil.rmtree(home + "/" + bd + "/" + filename)
        GLib.idle_add(refresh, self)
        GLib.idle_add(refresh_inner, self)
        GLib.idle_add(setProgress, self, 1)
        GLib.idle_add(callBox,self, "Config backups cleaned.", "Success!!")
    GLib.idle_add(self.button_toggles, True)
    GLib.idle_add(setProgress, self, 0)

def Delete_Inner_Backup(self):
    count = os.listdir(home + "/" + bd).__len__()

    if count > 0:
        GLib.idle_add(setProgress, self, 0.3)
        for filename in os.listdir(home + "/" + bd + "/" + self.backs.get_active_text()):
            if filename == self.backs_inner.get_active_text():
                if os.path.isdir(home + "/" + bd + "/" + self.backs.get_active_text() + "/" + filename):
                    shutil.rmtree(home + "/" + bd + "/" + self.backs.get_active_text() + "/" + filename)
                elif os.path.isfile(home + "/" + bd + "/" + self.backs.get_active_text() + "/" + filename):
                    os.unlink(home + "/" + bd + "/" + self.backs.get_active_text() + "/" + filename)
        GLib.idle_add(refresh_inner, self)
        GLib.idle_add(setProgress, self, 1)
        GLib.idle_add(callBox,self, "Config backups cleaned.", "Success!!")
    GLib.idle_add(self.button_toggles, True)
    GLib.idle_add(setProgress, self, 0)


# ===========================================
#		FLUSH ALL FUNCTION
# ===========================================
def Flush_All(self):
    count = os.listdir(home + "/" + bd).__len__()

    if count > 0:
        count = ((count/count)/count)
        GLib.idle_add(setMessage,self, "Deleting Backup")
        for filename in os.listdir(home + "/" + bd):                
            if os.path.isdir(home + "/" + bd + "/" + filename):
                GLib.idle_add(setProgress, self, self.progressbar.get_fraction() + count)
                shutil.rmtree(home + "/" + bd + "/" + filename)            
                

        GLib.idle_add(refresh, self)
        GLib.idle_add(refresh_inner, self)
        GLib.idle_add(callBox,self, ".SkelApp_Backups directory has been cleaned.", "Success!!")
        GLib.idle_add(setProgress, self, 0)
    GLib.idle_add(self.button_toggles, True)
    GLib.idle_add(setMessage,self, "Idle...")

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
    
    for item in BACKUPS_CATS:
        self.backs.append_text(item)

    self.backs.set_active(0)
    
def refresh_inner(self):
    count = os.listdir(home + "/" + bd).__len__()
    active_text = "".join([str(self.backs.get_active_text()), ""])

    if count > 0:
        if os.path.isdir(home + "/" + bd + "/" + active_text):
            self.backs_inner.get_model().clear()
            BACKUPS_FOLDER = []
            for filename in os.listdir(home + "/" + bd + "/" + active_text):
                BACKUPS_FOLDER.append(filename)
            for item in BACKUPS_FOLDER:
                self.backs_inner.append_text(item)

            self.backs_inner.set_active(0)
    else:
        self.backs_inner.get_model().clear()
        BACKUPS_FOLDER = []

def restore_inner(self):
    text = str(self.backs_inner.get_active_text())

    if text.__len__() > 0:
        path = home + "/" + bd + "/" + str(self.backs.get_active_text())
        regex = re.search(r'([\-\_].*)', text, re.IGNORECASE)
        
        
        GLib.idle_add(setMessage,self, "Restoring "  + text.replace(regex.group(0), ""))
        GLib.idle_add(setProgress, self, 0.1)
        if os.path.isfile(path + "/" + text):
            shutil.copy(path + "/" + text, home + "/" + text.replace(regex.group(0), ""))
        
        if os.path.isdir(path + "/" + text):
            count = os.listdir(path + "/" + text).__len__()

            if count > 0:
                count = ((count/count)/count)
                for folder in os.listdir(path + "/" + text):
                    if os.path.isdir(path + "/" + text + "/" + folder):
                        # print(home + "/" + text.replace(regex.group(0), "") + "/" + folder)
                        copytree(self, path + "/" + text + "/" + folder, home + "/" + text.replace(regex.group(0), "") + "/" + folder, True)
                    if os.path.isfile(path + "/" + text + "/" + folder):
                        shutil.copy(path + "/" + text + "/" + folder, home + "/" + text.replace(regex.group(0), "") + "/" + folder)
                    GLib.idle_add(setProgress, self, self.progressbar.get_fraction() + count)
                print(count)

        GLib.idle_add(setProgress, self, 1)
        GLib.idle_add(callBox,self, "Restore Complete", "Success!!")
        GLib.idle_add(setProgress, self, 0)
        GLib.idle_add(self.button_toggles, True)
        GLib.idle_add(setMessage,self, "Idle...")
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
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:
                print("ERROR3")
                self.ecode = 1

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
        
        copytree(self, home + '/.config', home + '/' + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + '/.config-backup-' +
                 now.strftime("%Y-%m-%d %H:%M:%S"), True)

        GLib.idle_add(setProgress, self, 0.3)

        # ============================
        #       LOACAL
        # ============================

        copytree(self, home + '/.local', home + '/' + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + '/.local-backup-' +
                 now.strftime("%Y-%m-%d %H:%M:%S"), True)
        GLib.idle_add(setProgress, self, 0.5)

        # ============================
        #       BASH
        # ============================
        if os.path.isfile(home + '/.bashrc'):
            shutil.copy(
                home + '/.bashrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.bashrc-backup-" +
                now.strftime("%Y-%m-%d %H:%M:%S"))
        
        # ============================
        #       ZSH
        # ============================
        if os.path.isfile(home + '/.zshrc'):
            shutil.copy(
                home + '/.zshrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.zshrc-backup-" +
                now.strftime("%Y-%m-%d %H:%M:%S"))

        # ============================
        #       CONKY
        # ============================
        if os.path.exists(home + '/.lua'):
            copytree(self, home + '/.lua', home + '/' + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + '/.lua-backup-' +
                    now.strftime("%Y-%m-%d %H:%M:%S"), True)

        if os.path.isfile(home + '/.conkyrc'):
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
                                home + '/.config/polybar/', True)
            print("Path copied")
 
    
    # ===========================================
    #		HERBSTLUFTWM
    # ===========================================
    elif cat == "herbstluftwm Configs":
        self.ecode = 0
        src = '/etc/skel/.config/herbstluftwm/'
        if not os.path.exists(src):
            self.ecode = 1
        else:
            copytree(self, src, home + '/.config/herbstluftwm/', True)
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
            copytree(self, src, home + '/.config/bspwm/', True)
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
            copytree(self, src1, home + '/.cache/i3lock', True)

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
                    copytree(self, src2 + "/" + filename, home + '/.local/share/' + filename, True)

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
            copytree(self, src1, home + '/.lua', True)
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
            copytree(self, src1, home + '/.config/dconf', True)

        print(".local copied")

    # ===========================================
    #		ROFI
    # ===========================================
    elif cat == "rofi Configs":
        self.ecode = 0
        src1 = '/etc/skel/.config/rofi'
        if not os.path.exists(src1):
            self.ecode = 1
        else:
            copytree(self, src1, home + '/.config/rofi', True)

        print("rofi copied")

    # ===========================================
    #		VARIETY
    # ===========================================
    elif cat == "Variety Configs":
        self.ecode = 0
        src1 = '/etc/skel/.config/variety'
        if not os.path.exists(src1):
            self.ecode = 1
        else:
            for folder in os.listdir(src1):
                if os.path.isdir(src1 + "/" + folder):
                    copytree(
                        self, src1 + "/" + folder, home + '/.config/variety/' + folder, True)
                elif os.path.isfile(src1 + "/" + folder):
                    shutil.copy(src1 + "/" + folder,
                                home + "/.config/variety/" + folder)

        print("variety copied")

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
                        self, src1 + "/" + folder, home + '/.config/xfce4/' + folder, True)
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
                    self, "/etc/skel/.config/" + item, home + '/.config/' + item, True)

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
            self.ecode = 1
        else:
            list = ["dunst","fontconfig","galculator","gtk-3.0","htop","nano","nomacs","qt5ct","ranger","rofi","volumeicon","mimeapps.list","Trolltech.conf","yad.conf"]
            for item in list:                
                if os.path.isdir("/etc/skel/.config/" + item):
                    copytree(
                        self, "/etc/skel/.config/" + item, home + '/.config/' + item, True)

                if os.path.isfile("/etc/skel/.config/" + item):
                    shutil.copy("/etc/skel/.config/" + item, home + "/.config/" + item)

            print("hlwm-config copied")

    else:
        if "," in cat:
            for filename in cat.split(','):
                old = filename.replace(" \'", "").replace("\'","").replace("[","").replace("]","")
                
                new = old.replace("/etc/skel",home)
                if os.path.isdir(old):
                    copytree(self, old, new, True)
                if os.path.isfile(old):
                    shutil.copy(old, new)
        else:
            self.ecode = 0
            old = cat.replace(" \'", "").replace("\'","").replace("[","").replace("]","")
            new = old.replace("/etc/skel",home)
            if os.path.isdir(old):
                copytree(self, old, new, True)
            if os.path.isfile(old):
                shutil.copy(old, new)
            
        
        

    setProgress(self,1)
    if(self.ecode == 1):
        callBox(self, "Cant seem to find that source. Have you got it installed?", "Success!!")
    else:
        callBox(self, "Skel executed successfully.", "Success!!")

    setProgress(self,0)
    self.button_toggles(True)
    setMessage(self, "Idle...")