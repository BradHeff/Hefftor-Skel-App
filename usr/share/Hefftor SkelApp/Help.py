import gi
from gi.repository import Gtk, GdkPixbuf, GLib
import os

base_dir = os.path.dirname(os.path.realpath(__file__))


class Help(Gtk.Window):
    def __init__(self):
        super(Help, self).__init__()
        sw = Gtk.ScrolledWindow()
        self.set_border_width(10)
        self.set_size_request(580, 400)
        self.set_resizable(False)
        self.set_icon_from_file(os.path.join(base_dir, 'hefftorlinux.svg'))
        self.set_position(Gtk.WindowPosition.NONE)

        self.connect("check_resize", self.on_check_resize)

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "Hefftors SkelApp Help"
        hb.props.subtitle = "How to use this application"
        self.set_titlebar(hb)

        self.hvbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        sw.add_with_viewport(self.hvbox)
        self.add(sw)

        # ===========================================
        #				HEADER Section
        # ===========================================
        self.listviewHDRH = Gtk.ListBox()
        self.listviewHDRH.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listviewHDRH, True, True, 0)

        # ListRow 1
        self.listRowHDRH = Gtk.ListBoxRow()
        self.hboxHDRH = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRowHDRH.add(self.hboxHDRH)

        self.pixbufH = GdkPixbuf.Pixbuf().new_from_file(
            os.path.join(base_dir, 'logo_help.png'))
        self.image = Gtk.Image().new_from_pixbuf(self.pixbufH)
        self.image_areaH = Gtk.Box()
        self.image_areaH.add(self.image)
        self.image_areaH.show_all()

        self.hboxHDRH.pack_start(self.image_areaH, True, True, 0)
        self.listviewHDRH.add(self.listRowHDRH)

        # ===========================================
        #				MENU Section
        # ===========================================
        self.listview1 = Gtk.ListBox()
        self.listview1.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listview1, True, True, 0)

        # ListRow 1
        self.listRow1 = Gtk.ListBoxRow()
        self.listRowTitle = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hboxTitle = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow1.add(self.hbox1)
        self.listRowTitle.add(self.hboxTitle)

        # ListRow 1 Elements
        self.labelTitle1 = Gtk.Label(xalign=0)
        self.labelTitle1.set_markup(
            "<span foreground='cyan' weight='bold' size='large' stretch='semiexpanded'>Step #1</span>")

        self.label1 = Gtk.Label(xalign=0)
        self.label1.set_line_wrap(True)
        self.label1.set_markup(
            "Select a category from the dropdown menu, this item selected will indicate what it is \
you want to apply from <span foreground='cyan' weight='bold'>/etc/skel</span> to your home directory")

        self.hboxTitle.pack_start(self.labelTitle1, False, False, 0)
        self.hbox1.pack_start(self.label1, False, False, 0)
        self.listview1.add(self.listRowTitle)
        self.listview1.add(self.listRow1)

        # ===========================================
        #				Example #2 Section
        # ===========================================
        self.listview2 = Gtk.ListBox()
        self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listview2, True, True, 0)

        # ListRow 2
        self.listRow2 = Gtk.ListBoxRow()
        self.hbox2 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow2.add(self.hbox2)

        # ListRow 2 Elements
        self.image1 = Gtk.Image()
        self.image1.set_from_file(
            os.path.join(base_dir, 'images/ex1.png'))

        self.hbox2.pack_start(self.image1, False, False, 0)
        self.listview2.add(self.listRow2)

        # ===========================================
        #				Example #3 Section
        # ===========================================
        self.listview3 = Gtk.ListBox()
        self.listview3.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listview3, True, True, 0)

        # ListRow 1
        self.listRow3 = Gtk.ListBoxRow()
        self.listRowTitle2 = Gtk.ListBoxRow()
        self.hbox3 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hboxTitle2 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow3.add(self.hbox3)
        self.listRowTitle2.add(self.hboxTitle2)

        # ListRow 1 Elements
        self.labelTitle2 = Gtk.Label(xalign=0)
        self.labelTitle2.set_markup(
            "<span foreground='cyan' weight='bold' size='large' stretch='semiexpanded'>Step #2</span>")

        self.label3 = Gtk.Label(xalign=0)
        self.label3.set_line_wrap(True)
        self.label3.set_markup(
            "Now that we have our category from the dropdown menu selected, its time we run the application. \
Click <span foreground='cyan' weight='bold'>Run Skel</span> button to apply the dotfiles from \
<span foreground='cyan' weight='bold'>/etc/skel</span> to your home directory")

        self.hboxTitle2.pack_start(self.labelTitle2, False, False, 0)
        self.hbox3.pack_start(self.label3, False, False, 0)
        self.listview3.add(self.listRowTitle2)
        self.listview3.add(self.listRow3)

        # ===========================================
        #				Example #4 Section
        # ===========================================
        self.listview4 = Gtk.ListBox()
        self.listview4.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listview4, True, True, 0)

        # ListRow 2
        self.listRow4 = Gtk.ListBoxRow()
        self.hbox4 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow4.add(self.hbox4)

        # ListRow 2 Elements
        self.image2 = Gtk.Image()
        self.image2.set_from_file(
            os.path.join(base_dir, 'images/ex2.png'))

        self.hbox4.pack_start(self.image2, False, False, 0)
        self.listview4.add(self.listRow4)

        # ===========================================
        #				Example #5 Section
        # ===========================================
        self.listview5 = Gtk.ListBox()
        self.listview5.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listview5, True, True, 0)

        # ListRow 1
        self.listRow5 = Gtk.ListBoxRow()
        self.listRowTitle3 = Gtk.ListBoxRow()
        self.hbox5 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hboxTitle3 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow5.add(self.hbox5)
        self.listRowTitle3.add(self.hboxTitle3)

        # ListRow 1 Elements
        self.labelTitle3 = Gtk.Label(xalign=0)
        self.labelTitle3.set_markup(
            "<span foreground='cyan' weight='bold' size='large' stretch='semiexpanded'><u>NOTE</u></span>")

        self.label5 = Gtk.Label(xalign=0)
        self.label5.set_line_wrap(True)
        self.label5.set_markup(
            "When the application is opened and you click <span foreground='cyan' weight='bold'>Run Skel</span> \
for the first time. The application will do a full backup of <span foreground='cyan' weight='bold'>.config, \
.local, .conkyrc and .bashrc</span>. The backups are listed in the backup section of the application.\n\
After selecting a backup from the dropdown list, Clicking <span foreground='cyan' weight='bold'>Delete\
</span> button will remove all backups contained within the backup directory for that hour.\n\
<span foreground='cyan' weight='bold' size='large' stretch='semiexpanded'><u>EXAMPLE</u></span>\n\
<b>Backup-2020-01-15 23</b>\n2020-01-15 = the date of the backup\n23 = the hour of the \
backup\nSo every backup made within that hour will be placed in that folder.")

        self.hboxTitle3.pack_start(self.labelTitle3, False, False, 0)
        self.hbox5.pack_start(self.label5, False, False, 0)
        self.listview5.add(self.listRowTitle3)
        self.listview5.add(self.listRow5)

        # ===========================================
        #				Example #6 Section
        # ===========================================
        self.listview6 = Gtk.ListBox()
        self.listview6.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hvbox.pack_start(self.listview6, True, True, 0)

        # ListRow 2
        self.listRow6 = Gtk.ListBoxRow()
        self.hbox6 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow6.add(self.hbox6)

        # ListRow 2 Elements
        self.image3 = Gtk.Image()
        self.image3.set_from_file(
            os.path.join(base_dir, 'images/ex3.png'))

        self.hbox6.pack_start(self.image3, False, False, 0)
        self.listview6.add(self.listRow6)

# ===============================================================================================================================

    def resizeImage(self, x, y):
        pixbuf = self.pixbufH.scale_simple(x, y,
                                           GdkPixbuf.InterpType.HYPER)
        self.image.set_from_pixbuf(pixbuf)

    def on_check_resize(self, window):
        boxAllocation = self.hboxHDRH.get_allocation()
        self.image_areaH.set_allocation(boxAllocation)
        self.resizeImage(boxAllocation.width,
                         boxAllocation.height)
