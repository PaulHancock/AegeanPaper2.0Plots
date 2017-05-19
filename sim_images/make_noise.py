__author__ = 'Paul Hancock'

from astropy.io import fits
import numpy as np
from scipy.ndimage.filters import gaussian_filter



noise_map = fits.open('bane.fits')
# TODO: Make the noise correlation vary with image position
noise = np.random.random(noise_map[0].data.shape)
noise = gaussian_filter(noise, sigma=5)
noise -= np.mean(noise)
noise /= np.std(noise)
noise_map[0].data = np.float32(noise)
noise_map.writeto('noise.fits', overwrite=True)


