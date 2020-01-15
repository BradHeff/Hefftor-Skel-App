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
        self.hbox1 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow1.add(self.hbox1)

        # ListRow 1 Elements
        self.label1 = Gtk.Label(xalign=0)
        self.label1.set_markup(
            "Select a category from the dropdown menu and click <span foreground=\"cyan\"><b>Run Skel</b></span> to update that\nspecific config from <span foreground=\"cyan\"><b>/etc/skel</b></span> to your home directory")

        self.hbox1.pack_start(self.label1, False, False, 0)
        self.listview1.add(self.listRow1)

        # ===========================================
        #				Example #1 Section
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


# ===================================================================================================================================

    def resizeImage(self, x, y):
        pixbuf = self.pixbufH.scale_simple(x, y,
                                           GdkPixbuf.InterpType.HYPER)
        self.image.set_from_pixbuf(pixbuf)

    def on_check_resize(self, window):
        boxAllocation = self.hboxHDRH.get_allocation()
        self.image_areaH.set_allocation(boxAllocation)
        self.resizeImage(boxAllocation.width,
                         boxAllocation.height)
