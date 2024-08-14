from kivymd.app import MDApp
from kivy.lang import Builder
from pyzbar.pyzbar import ZBarSymbol
from kivymd.uix.snackbar import Snackbar

KV = """
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
#:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol
MDBoxLayout:
	orientation:'vertical'
	ZBarCam:
		id:zbarcam
		code_types:ZBarSymbol.QRCODE.value,ZBarSymbol.EAN13.value
		on_symbols:app.on_symbols(*args)

"""


class Myapp(MDApp):
    def build(self):
        self.root = Builder.load_string(KV)

    def on_symbols(self, instance, symbols):
        if symbols != "":
            for symbol in symbols:
                print("YOu Qr is : ", symbol.data.decode())
                Snackbar(
                    text="You Qr is : {}".format(symbol.data.decode()),
                    md_bg_color="green",
                    font_size=25

                ).open()


if __name__ == "__main__":
    Myapp().run()
