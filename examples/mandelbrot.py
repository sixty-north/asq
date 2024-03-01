'''A conversion of Jon Skeet's LINQ Mandelbrot from LINQ to asq.

The original can be found at

http://msmvps.com/blogs/jon_skeet/archive/2008/02/26/visualising-the-mandelbrot-set-with-linq-yet-again.aspx

'''
import colorsys
from PIL import Image

from asq import query
from asq.initiators import integers


def generate(start, func):
    value = start
    while True:
        yield value
        value = func(value)


def colnorm(r, g, b):
    return (int(255 * r) - 1, int(255 * g) - 1, int(255 * b) - 1)


def col(n, max):
    if n == max:
        return (0, 0, 0)
    return colnorm(colorsys.hsv_to_rgb(0.0, 1.0, float(n) / max))


def mandelbrot():
    max_iterations = 200
    sample_width = 3.2
    sample_height = 2.5
    offset_x = -2.1
    offset_y = -1.25

    image_width = 480
    image_height = int(sample_height * image_width / sample_width)

    q = integers(0, image_height).select(lambda y: (y * sample_height) / image_height + offset_y) \
            .select_many_with_correspondence(
                lambda y: integers(0, image_width).select(lambda x: (x * sample_width) / image_width + offset_x),
                lambda y, x: (x, y)) \
            .select(lambda real_imag: complex(*real_imag)) \
            .select(lambda c: query(generate(c, lambda x: x * x + c))
                              .take_while(lambda x: x.real ** 2 + x.imag ** 2 < 4)
                              .take(max_iterations)
                              .count()) \
            .select(lambda c: ((c * 7) % 255, (c * 5) % 255, (c * 11) % 255) if c != max_iterations else (0, 0, 0))

    data = q.to_list()

    image = Image.new("RGB", (image_width, image_height))
    image.putdata(data)
    image.show()


if __name__ == '__main__':
    mandelbrot()
