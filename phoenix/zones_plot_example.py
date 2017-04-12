import numpy as np
from astropy.io import fits
from astropy.table import Table
from matplotlib import pyplot

image = fits.open('1997.fits')[0].data[0,0,:,:]
zones_bkg = fits.open('zones_bkg.fits')[0].data
zones_rms = fits.open('zones_rms.fits')[0].data
bane_bkg = fits.open("bane_bkg.fits")[0].data
bane_rms = fits.open('bane_rms.fits')[0].data

size = 250
pos = 925,2882
myslice = slice(pos[0]-size, pos[0]+size), pos[1]
kwargs = {'fontsize':18}

fig2 = pyplot.figure(figsize=(8,6))

ax2 = fig2.add_subplot(1,1,1)
ax2.plot( 1e3*(zones_bkg[myslice] + zones_rms[myslice]*5), 'g-')
ax2.plot( 1e3*(bane_bkg[myslice] + bane_rms[myslice]*5), 'r-')
ax2.plot( 1e3*(image[myslice]), 'b-')
ax2.set_xlabel('pixel coordinate', **kwargs)
ax2.set_ylabel('Flux density\n(mJy/Beam)', **kwargs)
ax2.set_xlim((200,500))
ax2.tick_params(axis='both', which='major', labelsize=16)
ax2.set_ylim((-2,5))
ax2.text(300,3.5, 'BANE', fontsize=16, rotation=-20)
ax2.text(355,1.7, 'Aegean', fontsize=16)
ax2.annotate('False\nPositive', xy=(255,3), xytext=(270,2), fontsize=16, arrowprops=dict(facecolor='black', shrink=0.05))
pyplot.savefig('false_detection.png')

#pyplot.show()
