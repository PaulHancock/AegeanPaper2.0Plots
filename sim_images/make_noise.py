__author__ = 'Paul Hancock'

from AegeanTools.fitting import elliptical_gaussian
from AegeanTools.wcs_helpers import WCSHelper, PSFHelper
from astropy.io import fits
import numpy as np
from scipy.ndimage.filters import gaussian_filter

sigma = 25e-6


def make_kern(size, a, b, pa):
    """
    Create a square smoothing kernel as an elliptical gaussian with the given parameters

    :param size: the size of the kernel in pixels
    :param a: semi-major axis in pixels
    :param b: semi-minor axis in pixels
    :param pa: position angle in degrees
    :return: a normalized kernel
    """
    # ensure that the size is odd
    if not (size % 2):
        size += 1
    shape = (size, size)
    xo, yo = np.indices(shape)
    amp, x, y, sx, sy, theta = 1, shape[0]/2, shape[1]/2, a, b, pa
    kernel = elliptical_gaussian(xo, yo, amp, x, y, sx, sy, theta)
    kernel /= np.sum(kernel)
    return kernel


def get_kernel(x, y, psf):
    beam = psf.get_pixbeam_pixel(x, y)
    a, b, pa = beam.a, beam.b, beam.pa
    return make_kern(5, a, b, pa)


def convolve(noise, psf):
    # Create a new array for the smoothed data
    smoothed = np.zeros_like(noise)
    # loop over the array
    print "convolve start"
    for i in xrange(1000):#noise.shape[0]):
        for j in xrange(1000):#noise.shape[1]):
            # at each pixel in the smoothed array we calculate the weighted average
            # get the convolution kernel and the indices into it
            kernel = get_kernel(i, j, psf)
            k, l = np.indices(kernel.shape)
            # the x,y need to be indices into the noise array
            # and we want this to be relative to the center of the kernel
            x = i + (k - kernel.shape[0]/2)
            y = j + (l - kernel.shape[1]/2)
            # mask out the pixels that are outside of the noise array
            mask = np.where((x < noise.shape[0]) & (x >= 0) & (y < noise.shape[1]) & (y >= 0))
            # the smoothed image at i,j is the weighted sum of the surrounding pixels
            smoothed[i, j] = np.sum(noise[x[mask], y[mask]]*kernel[k[mask], l[mask]])
        print "{0}/{1}".format(i, noise.shape[0])
    return smoothed


def main():
    # TODO:
    # make the noise vary as as if there are a bunch of tessellated observations
    # Each obs should have a different noise contribution
    # print "Creating noise with imprinted variation"
    noise_map = fits.open('bane.fits')

    print "Creating noise map"
    noise = np.random.normal(0,1,noise_map[0].data.shape)

    print "imprinting pattern onto noise"
    noise *= 1 + noise_map[0].data/255.
    noise_map[0].data = np.float32(noise)
    noise_map.writeto('temp.fits',overwrite=True)
    print "wrote temp.fits"

    print "Convolving with variable psf"
    wcsh = WCSHelper.from_file('bane.fits')
    psfh = PSFHelper('psf.fits', wcsh)
    smoothed = convolve(noise, psfh)

    print "writing file"
    noise_map[0].data = np.float32(smoothed)
    noise_map.writeto('noise.fits', overwrite=True)

if __name__ == "__main__":
    main()
