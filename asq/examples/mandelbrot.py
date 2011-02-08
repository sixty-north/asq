'''A conversion of Jon Skeet's LINQ Mandelbrot from LINQ to asq.

The original can be found at

http://msmvps.com/blogs/jon_skeet/archive/2008/02/26/visualising-the-mandelbrot-set-with-linq-yet-again.aspx

'''
import colorsys
import math
import Image

from asq.queryable import Queryable, asq

__author__ = 'rjs'

def generate(start, func):
    value = start
    while True:
        yield value
        value = func(value)

def colnorm((r,g,b)):
    return (int(255*r)-1,int(255*g)-1,int(255*b)-1)

def col(n,max):
    if n == max:
        return (0,0,0)
    return colnorm(colorsys.hsv_to_rgb(0.0,1.0,float(n)/max))

def mandelbrot():
    MaxIterations = 200
    SampleWidth = 3.2
    SampleHeight = 2.5
    OffsetX = -2.1
    OffsetY = -1.25

    ImageWidth = 480
    ImageHeight = int(SampleHeight * ImageWidth / SampleWidth)

    '''
                var query = from row in Enumerable.Range(0, ImageHeight)
                        from col in Enumerable.Range(0, ImageWidth)
                        // Work out the initial complex value from the row and column
                        let c = new Complex((col * SampleWidth) / ImageWidth + OffsetX,
                                            (row * SampleHeight) / ImageHeight + OffsetY)
                        // Work out the number of iterations
                        select Generate(c, x => x * x + c).TakeWhile(x => x.SquareLength < 4)
                                                          .Take(MaxIterations)
                                                          .Count() into count
                        // Map that to an appropriate byte value
                        select (byte)(count == MaxIterations ? 0 : (count % 255) + 1);
    '''

    query = Queryable.range(0, ImageHeight).select(lambda y: (y * SampleHeight) / ImageHeight + OffsetY) \
            .select_many_with_correspondence(
                lambda y: Queryable.range(0, ImageWidth).select(lambda x: (x * SampleWidth) / ImageWidth + OffsetX),
                lambda y, x: (x, y)) \
            .select(lambda real_imag: complex(*real_imag)) \
            .select(lambda c: asq(generate(c, lambda x: x * x + c))
                              .take_while(lambda x: x.real**2 + x.imag**2 < 4)
                              .take(MaxIterations)
                              .count()) \
            .select(lambda c: ((c * 7) % 255, (c * 5) % 255, (c * 11) % 255) if c != MaxIterations else (0, 0, 0))

    data = query.to_list()
    #print(data)

    image = Image.new("RGB", (ImageWidth, ImageHeight))
    image.putdata(data)
    image.show()

if __name__ == '__main__':
    mandelbrot()