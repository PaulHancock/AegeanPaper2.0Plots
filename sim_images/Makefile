
psf.fits: make_psf_map.py ../psf/mosaic_Week2_170-231MHz_psf.fits 
	python $<

noise.fits: make_noise.py bane_smooth.fits psf.fits
	python $<

catalogue.fits: make_catalogue.py psf.fits blank.fits
	python $<

SimulatedImage.fits: make_final_image.py moon.fits noise.fits model.fits
	python $<
