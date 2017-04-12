PLOTS = flux_err_hist.png flux_err.png pos_err.png pos_err_hist.png ab_err.png major_err_hist.png min_err_hist.png pa_err_hist.png

PYPLOTS = err_combined.png bias_combined.png

all: $(PLOTS) $(PYPLOTS)

clean:
	rm $(PLOTS) $(PYPLOTS)

err_combined.png bias_combined.png: pyplots.py ../All_fields_withC.fits ../All_fields_withoutC.fits ../All_fields_condon.fits
	python pyplots.py > results.dat

%.png: %.plt ../All_fields_withC.fits ../All_fields_withoutC.fits ../All_fields_condon.fits
	./$^ $@
