import numpy
from numpy import array
from numpy import linalg
from scipy.misc.pilutil import imsave, imread, imresize
 
 
def svd_encode(im, number_of_coefficients=50.0):
    img = im.astype('double')
    [rows, cols] = img.shape
    mindim = min(rows, cols)
    total = int(numpy.floor(number_of_coefficients * mindim / 100.0))
    [u, s, v] = linalg.svd(img)
    v = v.T
    compressed = numpy.zeros((rows, cols))
    for j in xrange(total):
        l = s[j] * numpy.matrix(u[:, j]).T
        vm = numpy.matrix(v[:, j])
        r = numpy.dot(l, vm)
        compressed = compressed + r
    compressed = numpy.floor(compressed)
    return compressed
 
 
# Testing
if __name__ == '__main__':
    imgs = ['peppers', 'lena', 'cameraman', 'rose']
    f = imread(imgs[0] + ".jpg", flatten=True)
    for i in xrange(5, 75, 15):
        f1 = svd_encode(f, float(i))
        imsave(imgs[0] + str(i) + ".jpg", f1)
    for im in imgs:
        print im + ".jpg"
        f = imread(im + ".jpg", flatten=True)
        g = svd_encode(f, 50)
        imsave(im + "_svd.jpg", g)
