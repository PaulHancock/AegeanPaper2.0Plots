from astropy.table import Table
from matplotlib import pyplot
import numpy as np

bp = Table.read('bane_prior_xm.vot')
fig = pyplot.figure()
ax1 = fig.add_subplot(1,1,1)
nbins = np.arange(-0.5,0.5,0.02)

mask = np.where((bp['err_peak_flux']>0) & (bp['err_peak_flux_2']>0))
ordering = np.argsort(bp['peak_flux'][mask])
data = bp['peak_flux'][mask]/bp['peak_flux_2'][mask]
errs = data * np.sqrt( np.hypot(bp['err_peak_flux'][mask]/bp['peak_flux'][mask],
                               bp['err_peak_flux_2'][mask]/bp['peak_flux_2'][mask]) )

data2 = (1-data)/errs
# compute a density normalised histogram and convert into a PDF
hist, _ = np.histogram(data2, density=True, bins=nbins)
hist /= np.sum(hist)
# plot
steps_y = np.ravel([ [a,a] for a in hist])
steps_x = np.ravel(zip(nbins[:-1], nbins[1:]))
ax1.fill_between(steps_x, 0, steps_y, alpha=0.5)
ax1.plot(steps_x, steps_y)

print np.median(data2), np.std(data2), np.sum(hist)
mu = np.mean(data2)
ax1.axvline(np.median(data2), color='k')
ax1.annotate('$\mu={0:-3.2f}$'.format(mu), xy=(mu,0.14), xytext=(0, 0.14), fontsize=14)
ax1.set_ylabel('PDF', fontsize=16)
ax1.set_xlabel('$(1-S_P/S_B)/err$', fontsize=16)
pyplot.savefig('priorized_hist.png')

