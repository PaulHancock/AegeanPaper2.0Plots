from astropy.io import fits
import astropy.units as u
from astropy.wcs import WCS
from matplotlib import pyplot
import numpy as np

sim = fits.open('SimulatedImage.fits')

fig = pyplot.figure(figsize=(10,10))
wcs = WCS(sim[0].header)
ax = fig.add_subplot(1,1,1,projection=wcs)
mpbl = ax.imshow(sim[0].data, origin='lower', vmin=-0.4, vmax=1, cmap='gray')
cax = fig.colorbar(mpbl, shrink=0.80)

cax.set_label("Flux density (Jy/beam)", fontsize=12)

ax.coords['ra'].set_ticks(np.arange(0,360,30)*u.degree)
ax.coords['ra'].set_ticklabel_visible(False)
ax.coords['dec'].set_ticks(np.arange(-90,30,30)*u.degree)
ax.coords['dec'].set_ticklabel_visible(False)
ax.grid(zorder=2)

fmt = {'color':'white', 'fontsize':12, 'xycoords':ax.get_transform('world'),
      'backgroundcolor':'black', 'zorder':4}

for ra in range(4,21,2):
    ax.annotate('{0:d}h'.format(ra),xy=[ra*15,-45], **fmt)

for dec in [-60,-30,0]:
    ax.annotate('{0:d}d'.format(dec),xy=[180,dec+1], **fmt)


pyplot.savefig('sim.png')
