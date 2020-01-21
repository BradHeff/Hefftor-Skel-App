#!/usr/bin/env python3
import Functions
import Help
import GUI
import shutil
from os.path import expanduser
import signal
import datetime
import threading
import re
import os
from gi.repository import Gtk, GdkPixbuf, GLib
import gi


gi.require_version('Gtk', '3.0')


home = expanduser("~")
BACKUPS_CATS = []
BACKUPS_FOLDER = []

bd = ".SkelApp_Backups"

actresses = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
             ('angelina jolie', 'los angeles',
                 '1975'), ('natalie portman', 'jerusalem', '1981'),
             ('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984')]


class HSApp(Gtk.Window):
    def __init__(self):
        super(HSApp, self).__init__()
        Gtk.Window.__init__(self, title="Hefftor SkelAp")
        # self.set_resizable(False)
        self.set_border_width(10)
        self.set_icon_from_file(os.path.join(
            GUI.base_dir, 'images/hefftorlinux.svg'))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        # self.connect("check_resize", self.on_check_resize)
        self.firstrun = 0
        self.ecode = 0
        self.browser = 0

        GUI.GUI(self, Gtk, GdkPixbuf, GLib)

# ===========================================================================================================

    def create_columns(self, treeView):

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", rendererText, text=0)
        column.set_sort_column_id(0)
        self.treeView.append_column(column)

    def toggled_cb(self, button):
        if self.rbutton2.get_active():
            self.treeView.set_sensitive(True)
            self.browse.set_sensitive(True)
            self.rbutton3.set_sensitive(True)
            self.rbutton4.set_sensitive(True)
            self.cat.set_sensitive(False)
            self.remove.set_sensitive(True)
            self.browser = 1
        else:
            self.treeView.set_sensitive(False)
            self.rbutton3.set_sensitive(False)
            self.rbutton4.set_sensitive(False)
            self.browse.set_sensitive(False)
            self.remove.set_sensitive(False)
            self.cat.set_sensitive(True)
            self.browser = 0

    # ===========================================
    #		REMOVE ITEMS TO TREEVIEW Section
    # ===========================================
    def on_remove_fixed(self, widget):
        selection = self.treeView.get_selection()
        model, paths = selection.get_selected_rows()

        # Get the TreeIter instance for each path
        for path in paths:
            iter = model.get_iter(path)
            # Remove the ListStore row referenced by iter
            model.remove(iter)

    # ===========================================
    #		ADD ITEMS TO TREEVIEW Section
    # ===========================================
    def on_browse_fixed(self, widget):
        if self.rbutton3.get_active():
            dialog = Gtk.FileChooserDialog(
                title="Please choose a file", action=Gtk.FileChooserAction.OPEN)
            dialog.set_select_multiple(True)
        elif self.rbutton4.get_active():
            dialog = Gtk.FileChooserDialog(
                title="Please choose a folder", action=Gtk.FileChooserAction.SELECT_FOLDER)
            dialog.set_select_multiple(True)
        dialog.set_current_folder("/etc/skel")
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            foldername = dialog.get_filenames()
            for item in foldername:
                self.store.append([item])

            # self.textBox.set_text(str(foldername))

            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            # print("Cancel clicked")
            dialog.destroy()

    # ===========================================
    #			HELP Section
    # ===========================================

    def on_help_clicked(self, widget):
        w = Help.Help()
        w.connect("delete-event", self.helpClose)
        w.show_all()
        self.btnhelp.set_sensitive(False)

    def helpClose(self, widget, signal):
        print("CLOSE MAIN HELP WINDOW")
        self.btnhelp.set_sensitive(True)

    # ===========================================
    #			RESTORE BACKUP Section
    # ===========================================

    def on_restore_inner_clicked(self, widget):
        self.button_toggles(False)
        t1 = threading.Thread(
            target=Functions.restore_inner, args=(self,))
        t1.daemon = True
        t1.start()
    # ===========================================
    #			DELETE BACKUP Section
    # ===========================================

    def on_delete_inner_clicked(self, widget):
        self.button_toggles(False)
        t1 = threading.Thread(
            target=Functions.Delete_Inner_Backup, args=(self,))
        t1.daemon = True
        t1.start()

    def on_delete_clicked(self, widget):
        self.button_toggles(False)
        t1 = threading.Thread(target=Functions.Delete_Backup, args=(self,))
        t1.daemon = True
        t1.start()

    # ===========================================
    #			REFRESH BACKUP Section
    # ===========================================

    def on_refresh_clicked(self, widget):
        Functions.refresh(self)

    def backs_changed(self, d):
        Functions.refresh_inner(self)

    # ===========================================
    #		DELETE ALL BACKUP Section
    # ===========================================

    def on_flush_clicked(self, widget):
        md = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.YES_NO, text="Are you Sure?")
        md.format_secondary_markup(
            "Are you sure you want to delete all your backups?")

        result = md.run()

        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            self.button_toggles(False)
            t1 = threading.Thread(target=Functions.Flush_All, args=(self,))
            t1.daemon = True
            t1.start()

    # ===========================================
    #			UPGRADE BASHRC Section
    # ===========================================

    def on_zshrc_skel_clicked(self, widget):
        self.button_toggles(False)
        t1 = threading.Thread(target=Functions.upgrade_zsh, args=(self,))
        t1.daemon = True
        t1.start()

    # ===========================================
    #			UPGRADE BASHRC Section
    # ===========================================

    def on_bashrc_skel_clicked(self, widget):
        self.button_toggles(False)
        t1 = threading.Thread(target=Functions.bash_upgrade, args=(self,))
        t1.daemon = True
        t1.start()

    # ===========================================
    #			RUN SKEL Section
    # ===========================================
    def on_button_fetch_clicked(self, widget):
        passes = True

        if not self.rbutton.get_active():
            # text = self.textBox.get_text()

            text = self.treeView.get_model()
            for item in text:
                if not "/etc/skel" in item[0]:
                    passes = False

        else:
            text = self.cat.get_active_text()

        if passes == True:

            self.button_toggles(False)
            if self.switch.get_active() and self.firstrun == 0:
                Functions.setMessage(self, "Running Backup")
                t1 = threading.Thread(target=Functions.processing,
                                      args=(self, text,))
                t1.daemon = True
                t1.start()
                self.firstrun = 1
            else:
                Functions.run(self, text)
        else:
            if not self.rbutton.get_active():
                Functions.callBox(
                    self, "It looks like your out of the /etc/skel directory", "Failed!!")

    def button_toggles(self, state):
        self.btn2.set_sensitive(state)
        self.btn7.set_sensitive(state)
        self.btn5.set_sensitive(state)
        self.btn9.set_sensitive(state)
        self.btn4.set_sensitive(state)
        self.btn10.set_sensitive(state)
        self.btn11.set_sensitive(state)
        if self.browser == 1:
            self.browse.set_sensitive(state)
            self.remove.set_sensitive(state)

# =========================================================================================================
#			                       FUNCTIONS Section
# =========================================================================================================

    # def resizeImage(self, x, y):
    #     pixbuf = self.pixbuf.scale_simple(x, y,
    #                                       GdkPixbuf.InterpType.HYPER)
    #     self.image.set_from_pixbuf(pixbuf)

    # def on_check_resize(self, window):
    #     boxAllocation = self.hboxHDR.get_allocation()
    #     self.image_area.set_allocation(boxAllocation)
    #     self.resizeImage(boxAllocation.width,
    #                      boxAllocation.height)
    def on_size_allocate(self, obj, rect):
        # skip if no pixbuf set
        if self.pixbuf is None:
            return

        # calculate proportions for image widget and for image
        k_pixbuf = float(self.pixbuf.props.height) / self.pixbuf.props.width
        k_rect = float(rect.height) / rect.width

        # recalculate new height and width
        if k_pixbuf < k_rect:
            newWidth = rect.width
            newHeight = int(newWidth * k_pixbuf)
        else:
            newHeight = rect.height
            newWidth = int(newHeight / k_pixbuf)

        # get internal image pixbuf and check that it not yet have new sizes
        # that's allow us to avoid endless size_allocate cycle
        base_pixbuf = self.image.get_pixbuf()
        if base_pixbuf.props.height == newHeight and base_pixbuf.props.width == newWidth:
            return

        # scale image
        base_pixbuf = self.pixbuf.scale_simple(
            newWidth,
            newHeight,
            GdkPixbuf.InterpType.BILINEAR
        )

        # set internal image pixbuf to scaled image
        self.image.set_from_pixbuf(base_pixbuf)

    # def on_image_resize(self, widget):
    #     allocation = self.hboxHDR.get_allocation()
    #     if self.temp_height != allocation.height or self.temp_width != allocation.width:
    #         self.temp_height = allocation.height
    #         self.temp_width = allocation.width
    #         pixbuf = self.pixbuf.scale_simple(
    #             allocation.width, allocation.height, GdkPixbuf.InterpType.BILINEAR)
    #         self.image.set_from_pixbuf(pixbuf)

# ============================================================================================================


def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!\nFreechoice Menu GUI is Closing.')
    Gtk.main_quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    window = HSApp()
    window.show_all()
    Gtk.main()
