from astropy.io import fits
import aplpy

phoenix = fits.open('1997.fits')
sim = fits.open('../MapF00E07.fits')

f = aplpy.FITSFigure(phoenix)
f.show_grayscale(vmin=-2e-4, vmax=1e-3, invert=True)
f.show_colorbar()
f.colorbar.set_axis_label_text('mJy/beam')
f.colorbar.set_axis_label_font(size=14)
f.axis_labels.set_font(size=12)
f.recenter(17.807125,-45.756191, radius=0.82 )
f.axis_labels.set_font(size=14)
f.save('phoenix.png')

f = aplpy.FITSFigure(sim)
f.show_grayscale(vmin=-2e-4, vmax=1e-3, invert=True)
f.show_colorbar()
f.colorbar.set_axis_label_text('mJy/beam')
f.colorbar.set_axis_label_font(size=14)
f.axis_labels.set_font(size=12)
f.axis_labels.set_font(size=14)
f.save('sim.png')
