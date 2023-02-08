from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy import platform
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar import pyzbar
import cv2


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1920)
        self.cam.set(4, 1080)
        self.img = Image()
        self.fps = 60

        buttonCode = "Button\n    id:'exitButton'\n    text:'Exit'\n    font_size:'30sp'\n    size_hint:(1,.2)\n    background_color: (1,0,0,1)\n    on_press:app.stop()"
        self.exitButton = Builder.load_string(buttonCode)

        self.outputtext = Label(text='', font_size='75px', size_hint=(1, .2), color=(1, 0, 0, 1))

        self.add_widget(self.img)
        self.add_widget(self.outputtext)
        self.add_widget(self.exitButton)
        Clock.schedule_interval(self.update, 1.0 / self.fps)

    def update(self, dt):
        if True:
            ret, frame = self.cam.read()

            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img.texture = image_texture

                barcodes = pyzbar.decode(frame)

                if barcodes == []:
                    scan_img = cv2.putText(frame, 'Scanning', (50, 75), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 2)
                    scan_buf = cv2.flip(scan_img, 0)
                    scan_buf = scan_buf.tobytes()
                    scan_texture = Texture.create(size=(scan_img.shape[1], scan_img.shape[0]), colorfmt='bgr')
                    scan_texture.blit_buffer(scan_buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.img.texture = scan_texture

                    self.outputtext.text = str('')
                    self.outputtext.color = (1, 0, 0, 1)

                else:
                    for barcode in barcodes:
                        (x, y, w, h) = barcode.rect
                        rectangle_img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 7)
                        rectangle_buf = cv2.flip(rectangle_img, 0)
                        rectangle_buf = rectangle_buf.tobytes()
                        rectangle_texture = Texture.create(size=(rectangle_img.shape[1], rectangle_img.shape[0]),
                                                           colorfmt='bgr')
                        rectangle_texture.blit_buffer(rectangle_buf, colorfmt='bgr', bufferfmt='ubyte')
                        self.img.texture = rectangle_texture

                        self.outputtext.text = str(barcode.data.decode("utf-8"))
                        self.outputtext.color = (0, 1, 0, 1)


class TestApp(App):
    def build(self):
        self.sm = ScreenManager(transition=SwapTransition())
        self.mainsc = MainScreen()
        scrn = Screen(name='main')
        scrn.add_widget(self.mainsc)
        self.sm.add_widget(scrn)

        return self.sm


if __name__ == '__main__':
    main_app = TestApp()
    main_app.run()
    cv2.destroyAllWindows()