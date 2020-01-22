import os
import Hefftor_SkelApp
from Hefftor_SkelApp import Functions

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
    "Variety Configs",
    "rofi Configs",
    "xfce Configs",
    "xfce-config package",
    "hlwm/bspwm configs package"
]


def GUI(self, Gtk, GdkPixbuf, GLib):
    hb = Gtk.HeaderBar()
    hb.props.show_close_button = True
    hb.props.title = "Hefftors SkelApp"
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

    # ===========================================
    #				HELP Section
    # ===========================================
    self.btnhelp = Gtk.Button(label="How to use SkelApp")
    self.btnhelp.connect("clicked", self.on_help_clicked)
    # self.vbox.pack_start(self.btnhelp, True, True, 0)

    # ListRow 1
    # self.temp_height = 0
    # self.temp_width = 0

    self.listRowHDR = Gtk.ListBoxRow()
    # box = Gtk.ScrolledWindow()

    self.hboxHDR = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.listRowHDR.add(self.hboxHDR)

    self.pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(base_dir, 'images/logo1.png'), 300, 50)
    self.image = Gtk.Image().new_from_pixbuf(self.pixbuf)
    # self.connect('check_resize', self.on_image_resize)

    # self.image.connect("size-allocate", self.on_size_allocate)

    # box.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    # box.add(self.image)
    self.hboxHDR.pack_start(self.image, False, False, 0)
    self.hboxHDR.pack_start(self.btnhelp, True, True, 0)
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
    self.hboxman = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.hboxchoose = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.vboxConfig = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.listRow1.add(self.vboxConfig)

    self.vboxConfig.pack_start(self.hbox1, True, True, 0)
    self.vboxConfig.pack_start(self.hboxman, True, True, 0)
    self.vboxConfig.pack_start(self.hboxchoose, True, True, 0)

    # ListRow 1 Elements
    # self.label1 = Gtk.Label(xalign=0)
    # self.label1.set_markup("<b>Select Category</b>")
    self.cat = Gtk.ComboBoxText()
    for CATS in MENU_CATS:
        self.cat.append_text(CATS)
    self.cat.set_active(0)
    self.cat.set_size_request(170, 0)

    self.rbutton = Gtk.RadioButton(label="Preconfigured")
    self.rbutton.connect("toggled", self.toggled_cb)
    self.rbutton2 = Gtk.RadioButton.new_from_widget(self.rbutton)
    self.rbutton2.set_label("Manual")
    self.rbutton2.connect("toggled", self.toggled_cb)
    self.rbutton2.set_active(False)

    self.rbutton3 = Gtk.RadioButton(label="File")
    self.rbutton4 = Gtk.RadioButton.new_from_widget(self.rbutton3)
    self.rbutton4.set_label("Folder")

    self.browse = Gtk.Button(label="ADD")
    self.browse.connect("clicked", self.on_browse_fixed)

    self.remove = Gtk.Button(label="REMOVE")
    self.remove.connect("clicked", self.on_remove_fixed)
    # self.textBox = Gtk.Entry()

    self.vbuttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    sw = Gtk.ScrolledWindow()
    sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
    sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    self.store = Gtk.ListStore(str)

    self.treeView = Gtk.TreeView(self.store)
    # treeView.connect("row-activated", self.on_activated)
    self.treeView.set_rules_hint(True)
    sw.set_size_request(270, 120)
    sw.add(self.treeView)
    self.create_columns(self.treeView)

    self.hbox1.pack_start(self.rbutton, False, False, 0)
    # self.hbox1.pack_start(self.label1, False, False, 0)
    self.hbox1.pack_end(self.cat, True, True, 0)

    self.hboxman.pack_start(self.rbutton2, False, False, 0)
    self.hboxman.pack_start(sw, True, True, 0)
    self.hboxman.pack_start(self.vbuttons, False, False, 0)

    self.hboxchoose.pack_start(self.rbutton3, True, False, 0)
    self.hboxchoose.pack_start(self.rbutton4, True, False, 0)

    self.vbuttons.pack_start(self.browse, False, False, 0)
    self.vbuttons.pack_start(self.remove, False, False, 0)
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
    self.listRow10 = Gtk.ListBoxRow()
    self.hbox4 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.hbox5 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.hbox9 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.hbox10 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.vbox11 = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.vboxDelete = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL, spacing=10)

    self.listRow4.add(self.vboxDelete)
    self.listRow5.add(self.hbox5)

    # ListRow 1 Elements
    self.backs = Gtk.ComboBoxText()
    Functions.refresh(self)
    self.backs.set_active(0)
    self.backs.set_size_request(170, 0)
    self.btn4 = Gtk.Button(label="Refresh")
    self.btn5 = Gtk.Button(label="Delete")
    self.btn9 = Gtk.Button(label="Clean All Backups")

    sw2 = Gtk.ScrolledWindow()
    sw2.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
    sw2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    self.store2 = Gtk.ListStore(str)

    self.treeView2 = Gtk.TreeView(self.store2)
    # treeView.connect("row-activated", self.on_activated)
    self.treeView2.set_rules_hint(True)
    sw2.set_size_request(270, 120)
    sw2.add(self.treeView2)
    self.create_columns(self.treeView2)

    # self.backs_inner = Gtk.ComboBoxText()
    Functions.refresh_inner(self)
    # self.backs_inner.set_active(0)
    # self.backs_inner.set_size_request(170, 0)
    self.btn10 = Gtk.Button(label="Delete")
    self.btn11 = Gtk.Button(label="Restore")

    self.btn4.connect("clicked", self.on_refresh_clicked)
    self.btn5.connect("clicked", self.on_delete_clicked)
    self.btn9.connect("clicked", self.on_flush_clicked)
    self.btn10.connect("clicked", self.on_delete_inner_clicked)
    self.btn11.connect("clicked", self.on_restore_inner_clicked)

    self.label4 = Gtk.Label(xalign=0)
    self.label4.set_markup("<b>Delete Backups</b>")

    self.hbox5.pack_start(self.label4, True, True, 0)
    self.hbox4.pack_start(self.backs, True, True, 0)
    self.hbox4.pack_start(self.btn4, False, False, 0)
    self.hbox4.pack_end(self.btn5, True, True, 0)

    # self.hbox10.pack_start(self.backs_inner, True, True, 0)
    self.hbox10.pack_start(sw2, True, True, 0)
    self.hbox10.pack_start(self.vbox11, False, False, 0)
    self.vbox11.pack_start(self.btn10, False, False, 0)
    self.vbox11.pack_start(self.btn11, False, False, 0)

    self.hbox9.pack_start(self.btn9, True, True, 0)
    # self.hbox10.pack_start(self.btn9, True, True, 0)

    self.listview4.add(self.listRow5)
    self.listview4.add(self.listRow4)

    self.vboxDelete.pack_start(self.hbox4, True, True, 0)
    self.vboxDelete.pack_start(self.hbox10, True, True, 0)
    self.vboxDelete.pack_start(self.hbox9, True, True, 0)

    self.backs.connect("changed", self.backs_changed)

    # ===========================================
    #				BASHRC Section
    # ===========================================
    self.listview2 = Gtk.ListBox()
    self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
    self.vbox.pack_start(self.listview2, True, True, 0)

    # ListRow 1
    self.listRow2 = Gtk.ListBoxRow()
    self.listRow7 = Gtk.ListBoxRow()
    self.vboxrc = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.hbox7 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.hbox8 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.listRow2.add(self.vboxrc)
    self.listRow7.add(self.hbox7)

    # ListRow 1 Elements
    self.label7 = Gtk.Label(xalign=0)
    self.label7.set_markup("<b>Apply New Shell RC</b>")
    self.btn7 = Gtk.Button(label="Run bashrc Upgrade")
    self.btn7.connect("clicked", self.on_bashrc_skel_clicked)
    self.btn8 = Gtk.Button(label="Run zshrc Upgrade")
    self.btn8.connect("clicked", self.on_zshrc_skel_clicked)

    self.vboxrc.pack_start(self.btn7, True, True, 0)
    self.vboxrc.pack_start(self.btn8, True, True, 0)
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
    self.hbox11 = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.vboxRun = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.listRow6.add(self.vboxRun)

    # ListRow 1 Elements
    self.btn2 = Gtk.Button(label="Run Skel")
    self.btn2.connect("clicked", self.on_button_fetch_clicked)
    self.label4 = Gtk.Label(xalign=0)
    self.label4.set_markup("<i>Idle...</i>")
    self.labelBacks = Gtk.Label(xalign=0)
    self.labelBacks.set_markup("<b>Run Backup Before Skel</b>")

    self.switch = Gtk.Switch()
    self.switch.set_active(True)

    self.hbox6.pack_end(self.btn2, True, True, 0)
    self.hbox6.pack_start(self.label4, True, True, 0)

    self.hbox11.pack_start(self.labelBacks, True, True, 0)
    self.hbox11.pack_start(self.switch, False, False, 0)

    self.listview6.add(self.listRow6)

    self.vboxRun.pack_start(self.hbox11, True, True, 0)
    self.vboxRun.pack_start(self.hbox6, True, True, 0)

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

    self.treeView.set_sensitive(False)
    self.browse.set_sensitive(False)
    self.remove.set_sensitive(False)
    self.rbutton3.set_sensitive(False)
    self.rbutton4.set_sensitive(False)
