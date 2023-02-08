import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import cv2
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from pyzbar import pyzbar


class OperationAreaBox(BoxLayout):
    pass


class ScanArea(BoxLayout):
    def __init__(self, **kwargs):
        super(ScanArea, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1920)
        self.cam.set(4, 1080)

        self.fps = 60
        self.schedule = None
        self.collected_strings = []

    def start_scanning(self):
        self.schedule = Clock.schedule_interval(self.update, 1.0 / self.fps)

    def stop_scanning(self):
        self.schedule.cancel()
        for _ in self.collected_strings:
            print(_)

    def update(self, dt):
        if True:
            ret, frame = self.cam.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

                self.ids.img.texture = image_texture

                barcodes = pyzbar.decode(frame)

                if not barcodes:
                    scan_img = cv2.putText(frame, 'Scanning', (50, 75), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 2)
                    scan_buf = cv2.flip(scan_img, 0)
                    scan_buf = scan_buf.tobytes()
                    scan_texture = Texture.create(size=(scan_img.shape[1], scan_img.shape[0]), colorfmt='bgr')
                    scan_texture.blit_buffer(scan_buf, colorfmt='bgr', bufferfmt='ubyte')

                    self.ids.img.texture = scan_texture

                else:
                    for barcode in barcodes:
                        (x, y, w, h) = barcode.rect
                        rectangle_img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 7)
                        rectangle_buf = cv2.flip(rectangle_img, 0)
                        rectangle_buf = rectangle_buf.tobytes()
                        rectangle_texture = Texture.create(size=(rectangle_img.shape[1], rectangle_img.shape[0]),
                                                           colorfmt='bgr')
                        rectangle_texture.blit_buffer(rectangle_buf, colorfmt='bgr', bufferfmt='ubyte')

                        self.ids.img.texture = rectangle_texture

                        actual_text = str(barcode.data.decode("utf-8"))
                        if actual_text not in self.collected_strings:
                            self.collected_strings.append(actual_text)


class OpAreaScan(OperationAreaBox):
    def __init__(self, **kwargs):
        super(OpAreaScan, self).__init__(**kwargs)

    def on_toggle_scan_qr(self, inst):
        if inst.state == "normal":
            self.ids.scan_area.stop_scanning()
            inst.text = "scanning stopped"
        else:
            self.ids.scan_area.start_scanning()
            inst.text = "scanning..."
        print("toggled camera on/off")


class AppObj(App):
    def __init__(self,
                 window_content: str,
                 app_title: str = "Sziller's App",
                 csm: float = 1.0):
        super(AppObj, self).__init__()
        self.title = app_title
        self.window_content = window_content
        self.content_size_multiplier = csm

    def build(self):
        return self.window_content

if __name__ == "__main__":
    from kivy.lang import Builder  # to freely pick kivy files

    display_settings = {0: {'fullscreen': False, 'run': Window.maximize},
                        1: {'fullscreen': False, 'size': (400, 800)},
                        2: {'fullscreen': False, 'size': (600, 400)},
                        3: {'fullscreen': False, 'size': (1000, 500)}}

    style_code = 1

    Window.fullscreen = display_settings[style_code]['fullscreen']
    if 'size' in display_settings[style_code].keys(): Window.size = display_settings[style_code]['size']
    if 'run' in display_settings[style_code].keys(): display_settings[style_code]['run']()

    try:
        content = Builder.load_file(str(sys.argv[1]))
    except IndexError:
        content = Builder.load_file("qr_reader.kv")

    application = AppObj(window_content=content,
                         app_title="QR code reader",
                         csm=1)
    application.run()
    cv2.destroyAllWindows()