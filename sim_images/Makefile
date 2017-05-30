# Edit this to be the path of your stilts.jar file
STILTS = java -jar ~/Software/stilts.jar

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
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@),$(subst _comp.fits,.reg,$@)

SimulatedImage_withC.fits : catalogue.fits SimulatedImage_withC_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='ra dec' values2='ra dec' out=$@ params=60

SimulatedImage_withoutC_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@),$(subst _comp.fits,.reg,$@) --nocov

SimulatedImage_withoutC.fits : catalogue.fits SimulatedImage_withoutC_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='ra dec' values2='ra dec' out=$@ params=60

SimulatedImage_condon_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@),$(subst _comp.fits,.reg,$@) --nocov --condon

SimulatedImage_condon.fits : catalogue.fits SimulatedImage_condon_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='ra dec' values2='ra dec' out=$@ params=60

err_combined.png bias_combined.png: pyplots.py SimulatedImage_withC.fits SimulatedImage_withoutC.fits SimulatedImage_condon.fits
	python pyplots.py > results.dat