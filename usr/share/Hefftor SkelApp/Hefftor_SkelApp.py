#!/usr/bin/env python3
import Functions
import Help

import threading
import datetime
import signal
from gi.repository import Gtk, GdkPixbuf, GLib
import gi
from os.path import expanduser
import os
import shutil


gi.require_version('Gtk', '3.0')


home = expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
MENU_CATS = [
    "polybar Configs",
    "herbstluftwm Configs",
    "bspwm Configs",
    "root Configs",
    "betterlockscreen cache",
    "Local Configs",
    "Conky Configs",
    "dconf Configs",
    "xfce Configs",
    "xfce-config package",
    "hlwm/bspwm configs package"
]
BACKUPS_CATS = []
bd = ".SkelApp_Backups"


class HSApp(Gtk.Window):
    def __init__(self):
        super(HSApp, self).__init__()
        Gtk.Window.__init__(self, title="Hefftor SkelAp")
        self.set_resizable(False)
        self.set_border_width(10)
        self.set_icon_from_file(os.path.join(base_dir, 'hefftorlinux.svg'))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.connect("check_resize", self.on_check_resize)
        self.firstrun = 0
        self.ecode = 0

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "Hefftors SkelApp"
        hb.props.subtitle = "Safely skel what needs to be skeled"
        self.set_titlebar(hb)

        self.vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        
        # ===========================================
        #				HELP Section
        # ===========================================
        self.btnhelp  = Gtk.Button(label="How to use SkelApp")
        self.btnhelp.connect("clicked", self.on_help_clicked)
        self.vbox.pack_start(self.btnhelp, True, True, 0)

        # ===========================================
        #				HEADER Section
        # ===========================================
        self.listviewHDR = Gtk.ListBox()
        self.listviewHDR.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listviewHDR, True, True, 0)

        # ListRow 1
        self.listRowHDR = Gtk.ListBoxRow()
        self.hboxHDR = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRowHDR.add(self.hboxHDR)

        self.pixbuf = GdkPixbuf.Pixbuf().new_from_file(
            os.path.join(base_dir, 'logo.png'))
        self.image = Gtk.Image().new_from_pixbuf(self.pixbuf)
        self.image_area = Gtk.Box()
        self.image_area.add(self.image)
        self.image_area.show_all()

        self.hboxHDR.pack_start(self.image_area, True, True, 0)
        self.listviewHDR.add(self.listRowHDR)

        # ===========================================
        #				MENU Section
        # ===========================================
        self.listview1 = Gtk.ListBox()
        self.listview1.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview1, True, True, 0)

        # ListRow 1
        self.listRow1 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow1.add(self.hbox1)

        # ListRow 1 Elements
        self.label1 = Gtk.Label(xalign=0)
        self.label1.set_markup("<b>Select Category</b>")
        self.cat = Gtk.ComboBoxText()
        for CATS in MENU_CATS:
            self.cat.append_text(CATS)
        self.cat.set_active(0)
        self.cat.set_size_request(170, 0)

        self.hbox1.pack_start(self.label1, False, False, 0)
        self.hbox1.pack_end(self.cat, True, True, 0)
        self.listview1.add(self.listRow1)

        # ===========================================
        #				BACKUPS Section
        # ===========================================
        self.listview4 = Gtk.ListBox()
        self.listview4.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview4, True, True, 0)

        # ListRow 1
        self.listRow4 = Gtk.ListBoxRow()
        self.listRow5 = Gtk.ListBoxRow()
        self.listRow9 = Gtk.ListBoxRow()
        self.hbox4 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hbox5 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hbox9 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow4.add(self.hbox4)
        self.listRow5.add(self.hbox5)
        self.listRow9.add(self.hbox9)

        # ListRow 1 Elements
        self.backs = Gtk.ComboBoxText()
        self.refresh()
        self.backs.set_active(0)
        self.backs.set_size_request(170, 0)
        self.btn4  = Gtk.Button(label="Refresh")
        self.btn5  = Gtk.Button(label="Delete")
        self.btn9  = Gtk.Button(label="Clean All Backups")

        self.btn4.connect("clicked", self.on_refresh_clicked)
        self.btn5.connect("clicked", self.on_delete_clicked)
        self.btn9.connect("clicked", self.on_flush_clicked)

        self.label4 = Gtk.Label(xalign=0)
        self.label4.set_markup("<b>Delete Backups</b>")
        
        self.hbox5.pack_start(self.label4, True, True, 0)
        self.hbox4.pack_start(self.backs, True, True, 0)
        self.hbox4.pack_start(self.btn4, False, False, 0)
        self.hbox4.pack_end(self.btn5, True, True, 0)
        self.hbox9.pack_start(self.btn9, True, True, 0)
        
        self.listview4.add(self.listRow5)
        self.listview4.add(self.listRow4)
        self.listview4.add(self.listRow9)

        # ===========================================
        #				BASHRC Section
        # ===========================================
        self.listview2 = Gtk.ListBox()
        self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview2, True, True, 0)

        # ListRow 1
        self.listRow2 = Gtk.ListBoxRow()
        self.listRow7 = Gtk.ListBoxRow()
        self.hbox2 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hbox7 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow2.add(self.hbox2)
        self.listRow7.add(self.hbox7)

        # ListRow 1 Elements
        self.label7 = Gtk.Label(xalign=0)
        self.label7.set_markup("<b>Apply New .bashrc</b>")
        self.btn7 = Gtk.Button(label="Run Bashrc Upgrade")
        self.btn7.connect("clicked", self.on_bashrc_skel_clicked)

        self.hbox2.pack_end(self.btn7, True, True, 0)
        self.hbox7.pack_start(self.label7, True, True, 0)
        self.listview2.add(self.listRow7)
        self.listview2.add(self.listRow2)

        # ===========================================
        #				RUN Section
        # ===========================================
        self.listview6 = Gtk.ListBox()
        self.listview6.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview6, True, True, 0)

        # ListRow 1
        self.listRow6 = Gtk.ListBoxRow()
        self.hbox6 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow6.add(self.hbox6)

        # ListRow 1 Elements
        self.btn2 = Gtk.Button(label="Run Skel")
        self.btn2.connect("clicked", self.on_button_fetch_clicked)
        self.label4 = Gtk.Label(xalign=0)
        self.label4.set_markup("<i>Idle...</i>")

        self.hbox6.pack_end(self.btn2, True, True, 0)
        self.hbox6.pack_start(self.label4, True, True, 0)
        self.listview6.add(self.listRow6)

        self.progressbar = Gtk.ProgressBar()
        self.vbox.pack_start(self.progressbar, True, True, 0)


        # ===========================================
        #				FOOTER Section
        # ===========================================
        self.listview3 = Gtk.ListBox()
        self.listview3.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview3, True, True, 0)

        # ListRow 1
        self.listRow3 = Gtk.ListBoxRow()
        self.hbox3 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow3.add(self.hbox3)

        # ListRow 1 Elements
        self.label3 = Gtk.Label(xalign=0)
        self.label3.set_text("Created By Brad Heffernan")

        self.hbox3.pack_start(self.label3, True, False, 0)
        self.listview3.add(self.listRow3)

#===========================================================================================================

    # ===========================================
    #			HELP Section
    # ===========================================
    def on_help_clicked(self, widget):
        w = Help.Help()
        w.show_all()

        #Functions.callBox(self, "Select a category from the dropdown menu and click <b>Run Skel</b> to\n update that specific config from <b>/etc/skel</b> to your home\n directory", "How it works.")


    # ===========================================
    #			DELETE BACKUP Section
    # ===========================================
    def on_delete_clicked(self, widget):
        for filename in os.listdir(home + "/" + bd):
            if filename == self.backs.get_active_text():
                shutil.rmtree(home + "/" + bd + "/" + filename)
        self.refresh()
        Functions.callBox(self, "Config backups cleaned.", "Success!!")

    # ===========================================
    #			REFRESH BACKUP Section
    # ===========================================
    def refresh(self):
        self.backs.get_model().clear()
        BACKUPS_CATS = []
        for filename in os.listdir(home + "/" + bd):
            if os.path.isdir(home + "/" + bd + "/" + filename):
                BACKUPS_CATS.append(filename)
        print(BACKUPS_CATS)
        for item in BACKUPS_CATS:
            self.backs.append_text(item)

        self.backs.set_active(0)

    def on_refresh_clicked(self, widget):
        self.refresh()
        

    # ===========================================
    #		DELETE ALL BACKUP Section
    # ===========================================
    def on_flush_clicked(self, widget):
        print("FLUSH!")
        for filename in os.listdir(home + "/" + bd):
            if os.path.isdir(home + "/" + bd + "/" + filename):
                shutil.rmtree(home + "/" + bd + "/" + filename)
        

        for filename in os.listdir(home + "/" + bd):
            if os.path.isfile(home + "/" + bd + "/" + filename):
                os.unlink(home + "/" + bd + "/" + filename)
        self.refresh()
        Functions.callBox(self, ".SkelApp_Backups directory has been cleaned.", "Success!!")

    # ===========================================
    #			UPGRADE BASHRC Section
    # ===========================================
    def on_bashrc_skel_clicked(self, widget):
        
        now = datetime.datetime.now()
        Functions.setMessage(self, "Running Backup")
        if not os.path.exists(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H")):
            os.makedirs(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"))
            
        shutil.copy(
            home + '/.bashrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.bashrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))
        shutil.copy(
            home + '/.inputrc', home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H") + "/.inputrc-backup-" +
            now.strftime("%Y-%m-%d %H:%M:%S"))
        
        GLib.idle_add(Functions.setMessage,self, "Done")
        shutil.copy("/etc/skel/.bashrc-latest", home + "/.bashrc")
        shutil.copy("/etc/skel/.bashrc-latest", home + "/.bashrc-latest")
        shutil.copy("/etc/skel/.inputrc-latest", home + "/.inputrc")
        shutil.copy("/etc/skel/.inputrc-latest", home + "/.inputrc-latest")
        Functions.callBox(self, "bashrc upgraded", "Success!!")
        Functions.setMessage(self, "Idle...")

    # ===========================================
    #			RUN SKEL Section
    # ===========================================
    def on_button_fetch_clicked(self, widget):

        self.btn2.set_sensitive(False)
        if self.firstrun == 0:
            Functions.setMessage(self, "Running Backup")

        t1 = threading.Thread(target=Functions.processing,
                              args=(self, self.cat.get_active_text(),))
        t1.daemon = True
        t1.start()


# =========================================================================================================
#			                       FUNCTIONS Section
# =========================================================================================================
    
    
    # ===========================================
    #		SKEL FUNCTION
    # ===========================================
    def run(self, cat):

        # ===========================================
        #		POLYBAR
        # ===========================================
        if cat == "polybar Configs":
            self.ecode = 0
            print(self.ecode)
            src = '/etc/skel/.config/polybar/'
            if not os.path.exists(src):
                self.ecode = 1
            else:
                Functions.copytree(self, src,
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
                Functions.copytree(self, src, home + '/.config/herbstluftwm/',
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
                Functions.copytree(self, src, home + '/.config/bspwm/'
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
                Functions.copytree(self, src1, home + '/.cache/i3lock')

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
                        Functions.copytree(self, src2 + "/" + filename, home + '/.local/share/' + filename)

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
                Functions.copytree(self, src1, home + '/.lua')
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
                Functions.copytree(self, src1, home + '/.config/dconf'
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
                        Functions.copytree(
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
                    Functions.copytree(
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
                        Functions.copytree(
                            self, "/etc/skel/.config/" + item, home + '/.config/' + item)

                    if os.path.isfile("/etc/skel/.config/" + item):
                        shutil.copy("/etc/skel/.config/" + item, home + "/.config/" + item)

                print("hlwm-config copied")

        Functions.setProgress(self,1)
        print("ErrorCode: ",self.ecode)
        if(self.ecode == 1):
            Functions.callBox(self, "Cant seem to find that source. Have you got it installed?", "Success!!")
        else:
            Functions.callBox(self, "Skel executed successfully.", "Success!!")

        Functions.setProgress(self,0)
        self.btn2.set_sensitive(True)
        Functions.setMessage(self, "Idle...")


    def resizeImage(self, x, y):
        pixbuf = self.pixbuf.scale_simple(x, y,
                                        GdkPixbuf.InterpType.HYPER)
        self.image.set_from_pixbuf(pixbuf)


    def on_check_resize(self, window):
        boxAllocation = self.hboxHDR.get_allocation()
        self.image_area.set_allocation(boxAllocation)
        self.resizeImage(boxAllocation.width,
                        boxAllocation.height)
#============================================================================================================


def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!\nFreechoice Menu GUI is Closing.')
    Gtk.main_quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    window = HSApp()
    window.show_all()
    Gtk.main()
