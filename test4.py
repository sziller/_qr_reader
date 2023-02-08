from kivy.app import App
from kivy.lang import Builder
from kivy_garden.zbarcam import ZBarCam

class QrCodeApp(App):

    def build(self):
        return Builder.load_file("qr_reader.kv")

if __name__ == "__main__":
    QrCodeApp().run()
