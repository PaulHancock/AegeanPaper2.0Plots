from astropy.io import fits
from matplotlib import pyplot
import numpy as np

temp = fits.open('mosaic_Week2_170-231MHz_psf.fits')

fig, axes = pyplot.subplots(3,1,figsize=(8,8))

def fix(ax):
    ax.set_xticks(range(0,361,60))
    ax.set_yticks(range(-90,91,30))
    ax.set_ylim((-90,45))
    ax.set_xticklabels([])
    ax.set_ylabel('Dec', fontsize=16)

labs = ['Major axis', 'Minor axis', 'Position angle']

for i,ax in enumerate(axes):
    data = temp[0].data
    mn,mx = np.nanmin(data[i,:,:]), np.nanmax(data[i,:,:])
    cax = ax.imshow(data[i,:,:], origin='lower', extent=(0,360,-90,90), vmin=mn, vmax=mx)
    cbar = fig.colorbar(cax, ax=ax)
    
    ticks = np.linspace(mn,mx, num=5)
    cbar.set_ticks(ticks)
    if i<2:
        tl = ['{0:3d}'.format(int(j)) for j in ticks*3600]
        cbar.set_ticklabels(tl)
        cbar.set_label('arcsec', fontsize=14)
    else:
        cbar.set_ticklabels([-90,-45,0,45,90])
        cbar.set_label('Degrees', fontsize=14)
    
    ax.text(240,20, labs[i], horizontalalignment='center', fontsize=18)
    fix(ax)

    ax.tick_params(axis='both', which='major', labelsize=12)
    

ax.set_xticklabels(range(0,361,60))
ax.set_xlabel('RA', fontsize=16)
pyplot.tight_layout()
pyplot.savefig('psf_maps.png')
