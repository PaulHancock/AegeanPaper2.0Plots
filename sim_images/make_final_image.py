#! python
__author__ = 'Paul Hancock'
__date__ = ''

from astropy.io import fits
import numpy as np
from scipy.ndimage import gaussian_filter


def main():
    # Load background image and normalise to be 0-1
    print "loading moon.fits"
    moon = fits.open('moon.fits')
    print "smoothing and re-scaling"
    background = gaussian_filter(moon[0].data/255., sigma=150)
    background -= np.min(background)
    background /= np.max(background)
    # background to have positive and negative components, with a magnitude of 10\sigma
    background = (background-0.5) * 10 * 0.1
    moon[0].data = background

    print "saving background.fits"
    moon.writeto('background.fits', overwrite=True)

    print "loading noise.fits/model.fits"
    # load the noise image
    rms = fits.open('noise.fits')[0].data

    # load the image with the sources in it
    model = fits.open('model.fits')
    print "constructing simulated image"
    model[0].data += background + rms
    model.writeto('SimulatedImage.fits', overwrite=True)
    print "done"

if __name__ == "__main__":
    main()