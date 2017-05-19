#! python
__author__ = 'Paul Hancock'
__date__ = ''

from astropy.io import fits
import numpy as np
from scipy.ndimage.filters import gaussian_filter

template = fits.open('../psf/mosaic_Week2_170-231MHz_psf.fits')


noise = gaussian_filter(np.random.random(template[0].data[0].shape), sigma=5, mode='wrap')
noise -= np.min(noise)
noise /= np.max(noise)

curve = np.abs(np.indices(noise.shape)[0] - noise.shape[0]/2) * 90/(noise.shape[0]/2)
curve = 1/np.cos(np.radians(curve))
curve[curve > 10] = np.nan  # mask the stupid regions

bmaj = 0.036 * curve * (1+noise/10.)
bmin = 0.036 * (1+noise/10.)
pa = 0 + (noise - 0.5)*10

template[0].data[0] = bmaj
template[0].data[1] = bmin
template[0].data[2] = pa
template[0].data = template[0].data[:3]
template.writeto('psf.fits', overwrite=True)
