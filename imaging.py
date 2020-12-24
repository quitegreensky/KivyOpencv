from kivy.graphics.texture import Texture
import cv2
import numpy as np 

class ImageProcessingBase:

    _colorfmt= None
    @property
    def colorfmt(self):
        return self._colorfmt
    
    @colorfmt.setter
    def colorfmt(self,fmt):
        self._colorfmt = fmt

    def __init__(self, image):
        self.cv_image = self.normalize_image(image)

        # Image is gray
        if len(self.cv_image.shape)==2:
            self.colorfmt = "GRAY"
            self.cv_image = self.cvt_colorfmt(self.cv_image, "BGR")

    def normalize_image(self, image):
        # is file path
        if isinstance(image, str):
            self.colorfmt = "BGRA"
            my_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        # kivy texture
        elif isinstance(image , Texture):
            self.colorfmt = "RGBA"
            my_image = self.texture2cv(image)
        #is already cv image
        elif isinstance(image ,np.ndarray):
            self.colorfmt = "BGRA"
            my_image = image
        else:
            raise TypeError
        return my_image

    def texture2cv(self, texture):
        width, height = texture.size
        pixels = texture.pixels
        newvalue = np.frombuffer(pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        newvalue = self.cvt_colorfmt(newvalue, "BGRA")
        return newvalue

    def cvt_colorfmt(self, src, mode):
        if self.colorfmt==mode:
            return src
        fmt = eval(f"cv2.COLOR_{self.colorfmt}2{mode}")
        src = cv2.cvtColor(src, fmt)
        self.colorfmt = mode
        return src


    def cv2texture(self):
        self.flip()
        src = self.cvt_colorfmt(self.cv_image, "RGBA")
        image_string = src.tostring()
        height, width = src.shape[:2]
        texture = Texture.create(size=(width, height), colorfmt="rgba")
        texture.blit_buffer(image_string, colorfmt = "rgba", bufferfmt="ubyte")
        return texture

    def show_image(self):
        cv2.imshow("image", self.cv_image)
        cv2.waitKey(0)

    def save(self, path):
        if cv2.imwrite(path, self.cv_image):
            return True
        else:
            return False

class ImageProcessing(ImageProcessingBase):
    """
    Example: 
        texture = ImageProcessing(path).resize(dsize=(0,0), fx=0.5, fy=0.5).contrast(1).brightness(50).cv2texture()
        self.root.ids.image.texture = texture
        texture = ImageProcessing(texture).flip().contrast(2).brightness(50).show_image()
    """

    def flip(self, code=0):
        self.cv_image= cv2.flip(self.cv_image, code)
        return self

    def resize(self, **kwargs):
        self.cv_image = cv2.resize(self.cv_image, **kwargs)
        return self 

    def contrast(self, contrast=1):
        """1.0-3.0"""
        self.cv_image = cv2.convertScaleAbs( self.cv_image, alpha=contrast)
        return self 

    def brightness(self, brightness=0):
        """0-100"""
        self.cv_image = cv2.convertScaleAbs( self.cv_image, beta=brightness)
        return self
    
    def grayscale(self):
        self.cv_image = self.cvt_colorfmt(self.cv_image, "GRAY")
        return self
