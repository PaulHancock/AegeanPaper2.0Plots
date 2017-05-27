
import AegeanTools
from AegeanTools import wcs_helpers
from astropy.io import fits
from astropy import table
import numpy as np


def dnds():
    # min/max flux in Jy
    smin = 0.1
    smax = 100
    # create a set of bins
    s = np.logspace(np.log10(smin), np.log10(smax), 200)
    # apply a scaling of S^{-3/2}
    ns = s**(-3./2)
    # multiply bt the bin width to get dN/dS = -3/2
    ns = ns[:-1] * (s[1:]-s[:-1])
    # normalise so the probability is 1
    ns /= np.sum(ns)
    return s, ns


def positions(n):
    # a bunch of sources get cut in this method so lets just make way too many
    nsrc = int(n * 2)
    x = np.random.uniform(low=-1, high=1, size=nsrc)
    y = np.random.uniform(low=-1, high=1, size=nsrc)
    # crop to a circle
    mask = np.where(x**2 + y**2 < 1)
    # rescale to be in degrees
    dec = y[mask]*90
    ra = (x[mask]/np.cos(np.radians(dec)))*180 + 180
    # remove things that have a dodgy ra
    mask2 = np.where((ra > 0) & (ra < 360))
    # now select just the number of sources that were requested
    ra = ra[mask2][:int(n)]
    dec = dec[mask2][:int(n)]
    return ra, dec


def get_shapes(pos):
    wcsheader = fits.getheader('blank.fits')
    wcs = wcs_helpers.WCSHelper.from_header(wcsheader)
    psf = wcs_helpers.PSFHelper('psf.fits', wcs)
    shapes = []
    for ra, dec in zip(*pos):
        a, b, pa = psf.get_psf_sky(ra, dec)
        shapes.append([a*3600, b*3600, pa])
    return np.array(shapes)


def make_catalogue(nsrc, outfile):
    nsrc = int(nsrc)
    pos = positions(nsrc)
    print "Made {0} sources".format(nsrc)
    s, prob = dnds()
    # Now we count how many sources we need in each bin to get the desired total number of sources
    counts = np.int32(np.ceil(prob * nsrc))
    # all sources in the same bin will have the same flux -> we have a discrete distribution of fluxes
    fluxes = []
    for n, i in zip(counts, s):
        fluxes.extend([i]*n)
    # we made too many sources thanks to np.ceil, so lets drop the faintest ones first
    fluxes = fluxes[-nsrc:]
    print "Made {0} fluxes".format(len(fluxes))
    shapes = get_shapes(pos)
    source = fits.Column(array=range(nsrc)*0, format='J', name='source')
    island = fits.Column(array=range(nsrc), format='J', name='island')
    a = fits.Column(array=shapes[:, 0], format='D', name='a')
    b = fits.Column(array=shapes[:, 1], format='D', name='b')
    pa = fits.Column(array=shapes[:, 2], format='D', name='pa')
    # the bmaj/bmin/bpa are the same as the a/b/pa -> we have only point sources
    bmaj = fits.Column(array=shapes[:, 0], format='D', name='psf_a')
    bmin = fits.Column(array=shapes[:, 1], format='D', name='psf_b')
    bpa = fits.Column(array=shapes[:, 2], format='D', name='psf_pa')

    ra = fits.Column(array=pos[0], format='D', name='ra')
    dec = fits.Column(array=pos[1], format='D', name='dec')
    flux = fits.Column(array=fluxes, format='D', name='peak_flux')
    tbhdu = fits.BinTableHDU.from_columns([island, source, ra, dec, flux, a, b, pa, bmaj, bmin, bpa])
    tbhdu.writeto(outfile, overwrite=True)


if __name__ == "__main__":
    make_catalogue(6e5, 'catalogue.fits')
