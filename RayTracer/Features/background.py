import math

import numpy as np
from features import *
import png


def clamp(color):
    # Ensures that a color component is between 0 and 255 inclusive
    x = math.ceil(color * 255)
    if 0 <= x <= 255:
        return x
    elif 0 > x:
        return 0
    else:
        return 255


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = np.full((height, width), fill_value=Color(0, 0, 0))

    def pixel_at(self, x, y):
        return self.pixels[y, x]

    def write_pixel(self, x, y, color):
        self.pixels[y, x] = color

    def to_png(self, path):
        """ forms a png image file from the canvas in the given directory.

        path: the path to the directory. if only the name of the file is given then the file will be stored in the
        current directory.
        """
        image = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                current_pixel = self.pixel_at(j, i)
                colors = [current_pixel.x, current_pixel.y, current_pixel.z]
                for color in colors:
                    row.append(clamp(color))
            image.append(row)

        f = open(path, 'wb')
        w = png.Writer(self.width, self.height, greyscale=False)
        w.write(f, image)
        f.close()
