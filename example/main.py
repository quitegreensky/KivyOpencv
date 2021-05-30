from kivy.lang import Builder
from kivymd.app import MDApp

import sys
sys.path.append("..")

from imaging import ImageProcessing
import cv2

KV = '''
Screen:

    Image:
        id: image
        size_hint: 0.5, 0.5
        pos_hint: {"center_x": .5, "center_y": .5}

'''


class MainApp(MDApp):
    def build(self):
        self.main = Builder.load_string(KV)
        return self.main

    def on_start(self):
        image = self.root.ids.image

        # # Load image from opencv
        # img = cv2.imread("image.png")
        # kv_texture = ImageProcessing(img).cv2texture()
        # image.texture = kv_texture

        # kivy texture to opencv
        image.source = "image.png"
        img = ImageProcessing(image.texture).texture2cv()
        cv2.imshow("image", img)
        cv2.waitKey(0)

MainApp().run()
