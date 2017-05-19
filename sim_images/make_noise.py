__author__ = 'Paul Hancock'

from astropy.io import fits
import numpy as np
from scipy.ndimage.filters import gaussian_filter

sigma = 25e-6

# TODO:
# make the noise vary as as if there are a bunch of tesselated observations
# Each obs should have a different noise contribution
noise_map = fits.open('bane.fits')
smoothed = gaussian_filter(noise_map[0].data/255., sigma=100)
smoothed -= np.min(smoothed)
smoothed /= np.max(smoothed)
noise_map[0].data = smoothed
noise_map.writeto('bane_smooth.fits', overwrite=True)

# TODO: Make the noise correlation vary with image position
noise = np.random.random(noise_map[0].data.shape)
noise = gaussian_filter(noise, sigma=5)
noise -= np.mean(noise)
noise /= np.std(noise)
noise *= sigma
noise *= (1+smoothed)

noise_map[0].data = np.float32(noise)
noise_map.writeto('noise.fits', overwrite=True)


