#! /usr/bin/env python
import os, sys
import astropy
from astropy.io import fits
from astropy.table import Table
import numpy as np
from matplotlib import pyplot


def make_err_plot(par, ax1=None, annotate=None, tabs=(None, None, None)):
    if ax1 is None:
        fig = pyplot.figure()
        ax1 = fig.add_subplot(1, 1, 1)
    nbins = np.arange(-2, 2, 0.1)

    print par
    for tab in tabs:
        if par == 'position':
            mask = np.where((tab['err_ra'] > 0) & (tab['err_dec'] > 0))
            # compute the z-score
            data = np.hypot((tab['ra_1'][mask] - tab['ra_2'][mask]) / tab['err_ra'][mask],
                            (tab['dec_1'][mask] - tab['dec_2'][mask]) / tab['err_dec'][mask]) / np.sqrt(2)
        else:
            mask = np.where((tab['err_{0}'.format(par)] > 0))
            data = np.abs(tab['{0}_1'.format(par)][mask] - tab['{0}_2'.format(par)][mask]) / tab['err_{0}'.format(par)][
                mask]
        data = np.log(data)
        # compute a density normalised histogram and convert into a PDF
        hist, _ = np.histogram(data, density=True, bins=nbins)
        hist /= np.sum(hist)
        # plot
        steps_y = np.ravel([[a, a] for a in hist])
        steps_x = np.ravel(zip(nbins[:-1], nbins[1:]))
        ax1.fill_between(steps_x, 0, steps_y, label=tab.title, alpha=0.5)
        ax1.plot(steps_x, steps_y)
        # median of data is the 'central' value, and should be 0.0
        # std of the data is the scatter in the fraction in dex
        # sum of the histogram should be 1 if we have correctly normalised the plot
        print "\t", tab.title
        print "\t\tmedian", 10 ** np.median(data)
        print "\t\tstd", 10 ** np.std(data)
    # remove the ytick labels
    ax1.set_yticklabels([])
    if annotate is not None:
        ymax = ax1.get_ylim()[1]
        ax1.text(1, 0.8 * ymax, annotate, fontsize=12)

    if ax1 is None:
        out_name = 'hist_comp_{0}.png'.format(par)
        pyplot.savefig(out_name)
        print "wrote {0}".format(out_name)
    return


def make_err_combined():
    withC = Table.read('SimulatedImage_withC.fits')
    withC.title = 'Errors from $J^TC^{-1}J$'
    withoutC = Table.read('SimulatedImage_withoutC.fits')
    withoutC.title = 'Errors from $J^TJ$'
    condon = Table.read('SimulatedImage_condon.fits')
    condon.title = "Errors from Condon'97"

    fig, ax = pyplot.subplots(3, 2, figsize=(8, 6))  # , sharex=True)
    for p, ax1, txt in zip(['position', 'peak_flux', 'a', 'b', 'pa'], ax.ravel(),
                           ['Position', '$S_p$', 'a', 'b', "PA"]):
        make_err_plot(p, ax1, txt, [withC, withoutC, condon])

    for i in range(3):
        ax[i, 0].set_ylabel('PDF', fontsize=14)

    ax[2, 0].set_xlabel('log(|$\Delta/\sigma$|)', fontsize=14)
    ax[1, 1].set_xlabel('log(|$\Delta/\sigma$|)', fontsize=14)

    # make the legend replace the unused subplot
    legend = pyplot.figlegend(*ax[2, 0].get_legend_handles_labels(), loc=[0.55, 0.11], fontsize=12)
    # hide the axes of the unused plot
    ax[2, 1].axis('off')
    pyplot.figtext(0.5, 0.9, s='Accuracy of reported uncertainties', fontsize=16, ha='center')
    pyplot.savefig('err_combined.png')


def make_bias_plot(par, ax1=None, annotate=None, tabs=(None, None)):
    if ax1 is None:
        fig = pyplot.figure()
        ax1 = fig.add_subplot(1, 1, 1)

    for i, tab in enumerate(tabs):
        mask = tab['err_{0}'.format(par)] > 0
        data = (tab['{0}_2'.format(par)] - tab['{0}_1'.format(par)])
        if par in ['ra', 'dec']:
            data /= tab['a_2'] / 3600 / 100  #3600
        else:
            data /= tab['{0}_2'.format(par)] / 100
        data = data[mask]
        fluxes = (tab['peak_flux_2'.format(par)] / tab['local_rms'])[mask]
        bins = np.logspace(np.log10(np.nanmin(fluxes)),
                           np.log10(np.nanmax(fluxes)), num=50)
        dig = np.digitize(fluxes, bins)
        means = np.array([np.mean(data[dig == j]) for j in range(len(bins))])
        ax1.plot(bins, means, label=tab.title)

    if par in ['a', 'b']:
        ax1.set_ylim((-8, 8))
    elif par in ['ra', 'dec']:
        ax1.set_ylim((-0.5, 0.5))
    elif par in ['peak_flux']:
        ax1.set_ylim((-5, 5))
    else:
        ylim = ax1.get_ylim()
        ymx = max(abs(ylim[0]), abs(ylim[1]))
        ax1.set_ylim((-ymx, ymx))

    if annotate is not None:
        ymax = ax1.get_ylim()[1]
        xmax = ax1.get_xlim()[1]
        ax1.text(1e2, 0.75 * ymax, annotate, fontsize=12)

    ax1.set_xscale('log')
    ax1.axhline(0, color='gray', alpha=0.7)
    return


def make_bias_combined():
    withC = Table.read('SimulatedImage_withC.fits')
    withC.title = 'Fitting with $C^{-1}$'
    withoutC = Table.read('SimulatedImage_withoutC.fits')
    withoutC.title = 'Fitting without $C^{-1}$'

    fig, ax = pyplot.subplots(3, 2, figsize=(8, 8), sharex=True)
    for p, ax1, txt in zip(['ra', 'dec', 'peak_flux', 'a', 'b', ], ax.ravel(),
                           ['RA (%)', 'Dec (%)', '$S_p$ (%)', 'a (%)', 'b (%)']):
        make_bias_plot(p, ax1, txt, (withC, withoutC))

    for i in range(3):
        ax[i, 0].set_ylabel('Bias', fontsize=14)

    ax[2, 0].set_xlabel('Measured SNR (Peak/RMS)', fontsize=14)
    ax[1, 1].set_xlabel('Measured SNR (Peak/RMS)', fontsize=14)

    # make the legend replace the unused subplot
    legend = pyplot.figlegend(*ax[2, 0].get_legend_handles_labels(), loc=[0.55, 0.11], fontsize=12)
    # hide the axes of the unused plot
    ax[2, 1].axis('off')
    ax[2, 0].set_xlim((5, 1e3))
    pyplot.figtext(0.5, 0.9, s='Fractional bias in fit parameters', fontsize=16, ha='center')
    pyplot.savefig('bias_combined.png')


if __name__ == "__main__":
    make_err_combined()
    make_bias_combined()

