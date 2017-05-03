from astropy.io import fits
import aplpy

def format(f):
    f.colorbar.set_axis_label_text('mJy/beam')
    f.colorbar.set_axis_label_font(size=14)
    f.axis_labels.set_font(size=12)
    f.axis_labels.set_font(size=14)
    f.ticks.show()
    f.ticks.set_color('black')
    f.tick_labels.set_xformat('hh:mm')
    f.tick_labels.set_yformat('dd:mm')
    f._ax1.tick_params(which='both', direction='in')
    f._ax2.tick_params(which='both', direction='in')
    
phoenix = fits.open('1997.fits')
phoenix[0].data *= 1e3
sim = fits.open('../MapF00E07.fits')
sim[0].data *= 1e3

f = aplpy.FITSFigure(phoenix)
f.show_grayscale(vmin=-0.2, vmax=1, invert=True)
f.show_colorbar()
f.recenter(17.807125,-45.756191, radius=0.82 )
format(f)
f.ticks.set_xspacing(0.25)
f.ticks.set_yspacing(0.25)
f.save('phoenix.png')

f = aplpy.FITSFigure(sim)
f.show_grayscale(vmin=-0.2, vmax=1, invert=True)
f.show_colorbar()
format(f)
f.ticks.set_xspacing(1)
f.ticks.set_yspacing(1)
f.save('sim.png')
