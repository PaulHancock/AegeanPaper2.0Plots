from astropy.io import fits
from astropy.table import Table
import aplpy

catalogue = Table.read('bane_comp.vot')
phoenix = fits.open('1997.fits')
phoenix[0].data *=1e3

is1 = catalogue[catalogue['island'] == 20]
is1 = (is1['ra'], is1['dec'], is1['a'][0]*2/3600, is1['b'][0]*2/3600, 90+is1['pa'][0])

is2 = catalogue[catalogue['island'] == 16]
is2 = list(zip(is2['ra'], is2['dec'], is2['a']*2/3600, is2['b']*2/3600, 90+is2['pa']))
print is1
print is2


f = aplpy.FITSFigure(phoenix, figsize=(8, 8))
f.show_grayscale(vmin=-0.2, vmax=1, invert=True)
f.recenter(17.562529, -46.246236, radius=0.02)

f.add_colorbar()
f.colorbar.set_axis_label_text('mJy/beam')
f.colorbar.set_axis_label_font(size=16)

#f.axis_labels.set_font(size=12)
f.axis_labels.set_font(size=16)

for i in is2:
    f.show_ellipses(*i, color='red', linewidth=2)
f.show_ellipses(*is1, color='yellow', linewidth=2)
f.save('overlaps.png')
