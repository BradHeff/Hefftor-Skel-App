#!/usr/bin/env python3

import threading
import datetime
import subprocess
from os.path import expanduser
import shutil
import signal
from gi.repository import Gtk, GdkPixbuf, GLib
import gi
import os
gi.require_version('Gtk', '3.0')

home = expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
MENU_CATS = ["polybar", "herbstluftwm",
             "bspwm", "bashrc-latest", "root configs", "locals", "xfce"]


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
        hb.props.title = "Hefftors Skel App"
        hb.props.subtitle = "Safely skel what needs to be skeled"
        self.set_titlebar(hb)

        self.vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

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
        #				First Section
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
        self.label1.set_text("Category")
        self.cat = Gtk.ComboBoxText()
        for CATS in MENU_CATS:
            self.cat.append_text(CATS)
        self.cat.set_active(0)
        self.cat.set_size_request(170, 0)

        self.hbox1.pack_start(self.label1, True, True, 0)
        self.hbox1.pack_end(self.cat, False, True, 0)
        self.listview1.add(self.listRow1)

        # ===========================================
        #				Second Section
        # ===========================================
        self.listview2 = Gtk.ListBox()
        self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview2, True, True, 0)

        # ListRow 1
        self.listRow2 = Gtk.ListBoxRow()
        self.hbox2 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow2.add(self.hbox2)

        # ListRow 1 Elements
        self.btn2 = Gtk.Button(label="Run")
        self.btn2.connect("clicked", self.on_button_fetch_clicked)
        self.label4 = Gtk.Label(xalign=0)
        self.label4.set_text("Idle...")

        self.hbox2.pack_end(self.btn2, False, False, 0)
        self.hbox2.pack_start(self.label4, False, True, 0)
        self.listview2.add(self.listRow2)

        self.progressbar = Gtk.ProgressBar()
        self.vbox.pack_start(self.progressbar, True, True, 0)
        # ===========================================
        #				Second Section
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

        self.hbox3.pack_start(self.label3, True, True, 0)
        self.listview3.add(self.listRow3)

    def setProgress(self, value):
        self.progressbar.set_fraction(value)

    def resizeImage(self, x, y):
        pixbuf = self.pixbuf.scale_simple(x, y,
                                          GdkPixbuf.InterpType.BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def on_check_resize(self, window):
        boxAllocation = self.hboxHDR.get_allocation()
        self.image_area.set_allocation(boxAllocation)
        self.resizeImage(boxAllocation.width,
                         boxAllocation.height)

    def on_button_fetch_clicked(self, widget):

        self.btn2.set_sensitive(False)
        if self.firstrun == 0:
            self.setMessage("Running Backup")

        t1 = threading.Thread(target=self.processing, args=())
        t1.daemon = True
        t1.start()

    def setMessage(self, message):
        self.label4.set_text(message)

    def processing(self):
        now = datetime.datetime.now()
        if self.firstrun == 0:
            GLib.idle_add(self.setProgress, 0.1)
            self.copytree(home + '/.config', home + '/.config_backup-' +
                          now.strftime("%Y-%m-%d %H:%M:%S"))
            GLib.idle_add(self.setProgress, 0.3)
            self.copytree(home + '/.local', home + '/.local_backup-' +
                          now.strftime("%Y-%m-%d %H:%M:%S"))
            GLib.idle_add(self.setProgress, 0.5)
            shutil.copy(
                home + '/.bashrc', home + "/.bashrc-backup-" +
                now.strftime("%Y-%m-%d %H:%M:%S"))
            self.firstrun = 1
            GLib.idle_add(self.setMessage, "Done")

        GLib.idle_add(self.setMessage, "Running Skel")
        GLib.idle_add(self.run)

    def run(self):
        self.setProgress(0.7)
        if self.cat.get_active_text() == "polybar":
            self.ecode = 0
            print(self.ecode)
            src = '/etc/skel/.config/polybar/'
            if not os.path.exists(src):
                self.ecode = 1
            else:
                self.copytree(src,
                              home + '/.config/polybar/')
                print("Path copied")

            print(self.ecode)
        elif self.cat.get_active_text() == "herbstluftwm":
            self.ecode = 0
            src = '/etc/skel/.config/herbstluftwm/'
            if not os.path.exists(src):
                self.ecode = 1
            else:
                self.copytree(src, home + '/.config/herbstluftwm/')
                print("Path copied")

        elif self.cat.get_active_text() == "bspwm":
            self.ecode = 0
            src = '/etc/skel/.config/bspwm/'
            if not os.path.exists(src):
                self.ecode = 1
            else:
                self.copytree(src, home + '/.config/bspwm/')
                print("Path copied")

        elif self.cat.get_active_text() == "bashrc-latest":
            self.ecode = 0

            src = '/etc/skel/.bashrc-latest'

            if not os.path.isfile(src):
                self.ecode = 1
            else:
                shutil.copy(
                    src, home + "/.bashrc-latest")
                print("Path of copied file")

        elif self.cat.get_active_text() == "root configs":
            self.ecode = 0
            src1 = '/etc/skel/.bashrc-latest'
            src2 = '/etc/skel/.dmrc'
            src3 = '/etc/skel/.face'
            src4 = '/etc/skel/.inputrc-latest'
            src5 = '/etc/skel/.xinitrc'
            src6 = '/etc/skel/.Xresources'
            src7 = '/etc/skel/.xsession'
            src8 = '/etc/skel/.xsessionrc'

            if not os.path.isfile(src1):
                self.ecode = 1
            else:
                shutil.copy(
                    src1, home + "/.bashrc-latest")

            if not os.path.isfile(src2):
                self.ecode = 1
            else:
                shutil.copy(
                    src2, home + "/.dmrc")

            if not os.path.isfile(src3):
                self.ecode = 1
            else:
                shutil.copy(
                    src3, home + "/.face")

            if not os.path.isfile(src4):
                self.ecode = 1
            else:
                shutil.copy(
                    src4, home + "/.inputrc-latest")

            if not os.path.isfile(src5):
                self.ecode = 1
            else:
                shutil.copy(
                    src5, home + "/.xinitrc")

            self.setProgress(0.8)

            if not os.path.isfile(src6):
                self.ecode = 1
            else:
                shutil.copy(
                    src6, home + "/.Xresources")

            if not os.path.isfile(src7):
                self.ecode = 1
            else:
                shutil.copy(
                    src7, home + "/.xsession")

            if not os.path.isfile(src8):
                self.ecode = 1
            else:
                shutil.copy(
                    src8, home + "/.xsessionrc")

            print("Root Configs copied")

        elif self.cat.get_active_text() == "locals":
            self.ecode = 0
            src1 = '/etc/skel/.local/share'
            if not os.path.exists(src1):
                self.ecode = 1
            else:
                self.copytree(src1, home + '/.local/share')

            src2 = '/etc/skel/.local/bin/'
            if not os.path.exists(src2):
                self.ecode = 1
            else:
                self.copytree(src2, home + '/.local/bin')
            print("Path copied")

        elif self.cat.get_active_text() == "xfce":
            self.ecode = 0
            src1 = '/etc/skel/.config/xfce4/panel'
            src2 = '/etc/skel/.config/xfce4/terminal'
            src3 = '/etc/skel/.config/xfce4/xfconf'

            src4 = '/etc/skel/.config/xfce4/helpers.rc'
            src5 = '/etc/skel/.config/xfce4/xfce4-screenshooter'
            src6 = '/etc/skel/.config/xfce4/xfce4-taskmanager.rc'

            if not os.path.exists(src1):
                self.ecode = 1
            else:
                self.copytree(src1, home + '/.config/xfce4/panel')

            if not os.path.exists(src2):
                self.ecode = 1
            else:
                self.copytree(src2, home + '/.config/xfce4/terminal')

            if not os.path.exists(src3):
                self.ecode = 1
            else:
                self.copytree(src3, home + '/.config/xfce4/xfconf')
            self.setProgress(0.8)
            if not os.path.isfile(src4):
                self.ecode = 1
            else:
                shutil.copy(
                    src4, home + "/.config/xfce4/helpers.rc")

            if not os.path.isfile(src5):
                self.ecode = 1
            else:
                shutil.copy(
                    src5, home + "/.config/xfce4/xfce4-screenshooter")

            if not os.path.isfile(src6):
                self.ecode = 1
            else:
                shutil.copy(
                    src6, home + "/.config/xfce4/xfce4-taskmanager.rc")
            print("xfce copied")

        self.setProgress(1)
        if(self.ecode == 1):
            self.callBox(1)
        else:
            self.callBox(0)
        self.setProgress(0)
        self.btn2.set_sensitive(True)
        self.setMessage("Idle...")

    def callBox(self, errorCode):
        if errorCode == 0:
            message = "Skel executed successfully."
            title = "Success!!"
        else:
            title = "Error!!"
            message = "Cant seem to find that source. Have you got it installed?"

        md = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.OK, text=title)
        md.format_secondary_text(message)
        md.run()
        md.destroy()
        # self.set_sensitive(True)

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
                except:
                    print("ERROR2")
                    self.ecode = 1
            else:
                try:
                    shutil.copy2(s, d)
                except:
                    print("ERROR3")
                    self.ecode = 1


def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!\nFreechoice Menu GUI is Closing.')
    Gtk.main_quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    window = HSApp()
    window.show_all()
    Gtk.main()
