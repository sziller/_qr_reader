import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy_garden.zbarcam import ZBarCam

class AppObj(App):
    def __init__(self,
                 window_content: str,
                 app_title: str = "Sziller's App",
                 csm: float = 1.0):
        super(AppObj, self).__init__()
        self.window_content = window_content

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
                         app_title="QR code generator",
                         csm=1)
    application.run()