
psf.fits: make_psf_map.py ../psf/mosaic_Week2_170-231MHz_psf.fits 
	python $<

noise.fits: make_noise.py bane.fits
	python $<

catalogue.fits: make_catalogue.py psf.fits blank.fits
	python $<