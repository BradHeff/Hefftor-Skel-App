from gi.repository import Gtk, GdkPixbuf, GLib
import gi


class ImageX(Gtk.Image):
    pixbuf = None

    def __init__(self, *args, **kwargs):
        super(ImageX, self).__init__(*args, **kwargs)
        self.connect("size-allocate", self.on_size_allocate)

    def set_pixbuf(self, pixbuf):
        """
        use this function instead set_from_pixbuf
        it sets additional pixbuf, which allows to implement autoscaling
        """
        self.pixbuf = pixbuf
        self.set_from_pixbuf(pixbuf)

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
        base_pixbuf = self.get_pixbuf()
        if base_pixbuf.props.height == newHeight and base_pixbuf.props.width == newWidth:
            return

        # scale image
        base_pixbuf = self.pixbuf.scale_simple(
            newWidth,
            newHeight,
            GdkPixbuf.InterpType.BILINEAR
        )

        # set internal image pixbuf to scaled image
        self.set_from_pixbuf(base_pixbuf)
