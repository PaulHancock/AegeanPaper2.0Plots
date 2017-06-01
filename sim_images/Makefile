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
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@),$(subst _comp.fits,.reg,$@) --island

SimulatedImage_withC.fits : catalogue.fits SimulatedImage_withC_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='ra dec' values2='ra dec' out=$@ params=60

SimulatedImage_withoutC_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@),$(subst _comp.fits,.reg,$@) --nocov --island

SimulatedImage_withoutC.fits : catalogue.fits SimulatedImage_withoutC_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='ra dec' values2='ra dec' out=$@ params=60

SimulatedImage_condon_comp.fits: SimulatedImage.fits SimulatedImage_bkg.fits SimulatedImage_rms.fits
	aegean --autoload $< --psf psf.fits --table $(subst _comp,,$@),$(subst _comp.fits,.reg,$@) --nocov --condon --island

SimulatedImage_condon.fits : catalogue.fits SimulatedImage_condon_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='ra dec' values2='ra dec' out=$@ params=60

err_combined.png bias_combined.png: pyplots.py SimulatedImage_withC.fits SimulatedImage_withoutC.fits SimulatedImage_condon.fits
	python pyplots.py > results.dat
	convert err_combined.png -trim err_combined.png
	convert bias_combined.png -trim bias_combined.png

sim.png: SimulatedImage.fits
	 ~/Software/DS9/ds9 -single $< -cmap gray \
	-zoom to fit -zoom to 0.04 -scale limits -0.5 1 \
	-grid yes -grid type publication -grid axes type exterior \
	-grid numerics no -grid title no -grid labels no \
	-grid grid yes -grid grid color white -grid axes color white -colorbar off \
	-grid border color black -grid title no \
	-saveimage $@ -exit
	convert $@ -trim $@