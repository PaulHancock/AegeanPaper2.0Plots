
psf.fits: make_psf_map.py ../psf/mosaic_Week2_170-231MHz_psf.fits 
	python $<

noise.fits: make_noise.py bane_smooth.fits psf.fits
	python $<

catalogue.fits: make_catalogue.py psf.fits blank.fits
	python $<

SimulatedImage.fits: make_final_image.py moon.fits noise.fits model.fits
	python $<

SimulatedImage_bkg.fits SimulatedImage_rms.fits: SimulatedImage.fits
	BANE $<

SimulatedImage_withC_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@)

SimulatedImage_withoutC_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@) --nocov

SimulatedImage_condon_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@) --nocov --condon