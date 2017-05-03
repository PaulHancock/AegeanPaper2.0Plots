from astropy.io import fits
from astropy.table import Table
import aplpy
import numpy as np
import matplotlib.pyplot as pyplot
import sys

def format(f):
    f.show_grayscale(vmin=0, vmax=1, invert=True)
    f.recenter(18.430477,-45.345189, radius=0.3 )

    f.show_colorbar()
    f.colorbar.set_axis_label_text('RMS (mJy/beam)')
    f.colorbar.set_axis_label_font(size=14)
    
    f.axis_labels.set_font(size=12)
    f.axis_labels.set_font(size=14)
    f.ticks.show()
    f.ticks.set_color('black')
    f.ticks.set_xspacing(0.25)
    f.tick_labels.set_xformat('hh:mm')
    f.tick_labels.set_yformat('dd:mm')
    f._ax1.tick_params(which='both', direction='in')
    f._ax2.tick_params(which='both', direction='in')

    return

catalogue = Table.read('false_positives.vot')

fig = pyplot.figure(figsize=(6,8))

zones = fits.open('zones_rms.fits')
zones[0].data *= 1e3
f = aplpy.FITSFigure(zones, figure=fig, subplot=(2,1,1))
format(f)
f.show_markers(catalogue['ra'].data,catalogue['dec'].data, color='red', marker='X')
f.show_circles(18.642292, -45.252981, radius=0.02, color='yellow')
#f.tick_labels.hide_x()
#f.axis_labels.hide_x()
f.add_label(18.7, -45.1, 'Zones', size=14)

grid = fits.open('bane_rms.fits')
grid[0].data = np.squeeze(grid[0].data)*1e3
# slices=[0,1] is required because the FITS header reports more than 2 axes 
# and aplpy is too stupid to notice that the extra axes are empty
f = aplpy.FITSFigure(grid, figure=fig, subplot=(2,1,2), slices=[0,1])
format(f)
#f.show_markers(catalogue['ra'].data,catalogue['dec'].data, color='red', marker='X')
f.show_circles(18.642292, -45.252981, radius=0.02, color='yellow')
f.add_label(18.7, -45.1, 'Grid', size=14)

pyplot.savefig('false_positives.png')


