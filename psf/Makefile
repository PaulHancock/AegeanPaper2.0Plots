STILTS = java -jar ~/Software/stilts.jar

ALL = mosaic_Week2_170-231MHz_psf.fits psf_maps.png

mosaic_Week%_170-231MHz_psf.fits:
	wget -O $@ http://store02.icrar.org:7777/RETRIEVE?file_id=$@

psf_maps.png: psf_plot.py mosaic_Week2_170-231MHz_psf.fits
	python $<

.PHONY: all
all: $(ALL) FORCE

FORCE: