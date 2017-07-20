from astropy.table import Table
from matplotlib import pyplot
import numpy as np

bp = Table.read('blind_prior_xm.fits')
fig = pyplot.figure()
ax1 = fig.add_subplot(1, 1, 1)
mx = 30
nbins = np.arange(-1*mx, mx, mx/100.)

err_mask = np.where((bp['err_peak_flux_blind'] > 0) & (bp['err_peak_flux_prior'] > 0))
data = (bp['peak_flux_blind'][err_mask]-bp['peak_flux_prior'][err_mask])/bp['peak_flux_blind'][err_mask] * 100
# compute a density normalised histogram and convert into a PDF
hist, _ = np.histogram(data, density=True, bins=nbins)
hist /= np.sum(hist)
# plot
steps_y = np.ravel([[a, a] for a in hist])
steps_x = np.ravel(zip(nbins[:-1], nbins[1:]))
ax1.fill_between(steps_x, 0, steps_y, alpha=0.5)
ax1.plot(steps_x, steps_y)
ax1.set_yscale('log')

plot_mask = np.where((data < mx) & (data > -1*mx))
print np.median(data[plot_mask]), np.mean(data[plot_mask]), np.std(data[plot_mask]), np.sum(hist)
mu = np.median(data[plot_mask])
sigma = np.std(data[plot_mask])
y = np.max(hist)*0.1

ax1.axvline(np.median(data), color='k')
ax1.annotate('$\mu={0:-3.2g}$%\n$\sigma={1:-3.2g}$%'.format(mu, sigma), xy=(mu+mx/5, y), xytext=(mu+mx/5, y), fontsize=14)
ax1.set_ylabel('PDF', fontsize=16)
ax1.set_xlabel('$(S_B-S_P)/S_B$ (%)', fontsize=16)
pyplot.savefig('priorized_hist.png')

