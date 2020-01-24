import gi
import os
from threading import Thread
from time import sleep
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
base_dir = os.path.dirname(os.path.realpath(__file__))
class Splash(Thread):
    def __init__(self):
        super(Splash, self).__init__()

        # Create a popup window
        self.window = Gtk.Window(Gtk.WindowType.POPUP)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect('destroy', Gtk.main_quit)
        self.window.set_default_size(400, 250)

        # Add box and label
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        pixbuf = GdkPixbuf.Pixbuf().new_from_file(os.path.join(base_dir, 'images/SkelApp_Splash.png'))
        image = Gtk.Image().new_from_pixbuf(pixbuf)        
        
        self.progress = Gtk.ProgressBar()
        box.pack_start(image, True, True, 0)
        # box.pack_start(self.progress, False, False, 0)
        self.window.add(box)

    def run(self):
        # Show the splash screen without causing startup notification
        # https://developer.gnome.org/gtk3/stable/GtkWindow.html#gtk-window-set-auto-startup-notification
        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)

        # Need to call Gtk.main to draw all widgets
        Gtk.main()

    def destroy(self):
        self.window.destroy()