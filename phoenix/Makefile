STILTS = java -jar ~/Software/stilts.jar

AUXFILES = bane_bkg.fits bane_rms.fits zones_rms.fits zones_bkg.fits

CATALOGUES = bane_comp.vot bane_comp.reg zones_comp.vot zones_comp.reg false_positives.vot false_positives.reg prior_comp.vot bane_prior_xm.vot 

PLOTS = priorized_hist.png phoenix.png sim.png overlaps.png ds9.png mask.png false_detection.png false_positives.png

MIMAS = mask.mim mask.reg 

aux: $(AUXFILES)

cat: $(CATALOGUES)

all: 1997.fits aux cat $(MIMAS) $(PLOTS)

clean: FORCE
	rm $(AUXFILES) $(CATALOGUES) $(MIMAS) $(PLOTS)

1997.fits:
	wget -O $@ https://zenodo.org/record/439996/files/1997.fits

bane_bkg.fits bane_rms.fits: 1997.fits
	BANE 1997.fits --out=bane

zones_bkg.fits zones_rms.fits: 1997.fits
	aegean 1997.fits --save
	rm 1997_crv.fits
	mv 1997_bkg.fits zones_bkg.fits
	mv 1997_rms.fits zones_rms.fits

bane_comp.vot bane_comp.reg: 1997.fits bane_bkg.fits bane_rms.fits
	aegean 1997.fits --background bane_bkg.fits --noise bane_rms.fits --table bane.vot,bane.reg

zones_comp.vot zones_comp.reg: 1997.fits zones_bkg.fits zones_rms.fits
	aegean 1997.fits --background zones_bkg.fits --noise zones_rms.fits --table zones.vot,zones.reg


false_positives.vot: zones_comp.vot bane_comp.vot
	$(STILTS) tmatch2 find=best matcher=sky params=5 \
	in1=zones_comp.vot values1='ra dec' \
	in2=bane_comp.vot values2='ra dec' \
	join=1not2 out=$@

false_positives.reg: false_positives.vot
	echo '#Region file format: DS9 version 4.1' > $@ 
	echo 'global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1' >> $@
	$(STILTS) tpipe cmd='keepcols "ra_str dec_str"' in=false_positives.vot | grep --line-buffered '^|.*:' | awk '{print "point("$$2","$$4") # point=x"}' >> $@

false_detection.png: zones_plot_example.py 1997.fits zones_bkg.fits zones_rms.fits bane_bkg.fits bane_rms.fits
	python $<
	convert $@ -trim $@

false_positives.png: false_positives.py zones_rms.fits bane_rms.fits false_positives.vot
	python $<
	convert $@ -trim $@

prior_comp.vot: bane_comp.vot 1997.fits
	aegean --priorized=1 --input=bane_comp.vot --table=prior.vot 1997.fits

bane_prior_xm.vot: prior_comp.vot bane_comp.vot
	$(STILTS) tmatch2 find=best matcher=sky params=60 \
	in1=bane_comp.vot values1='ra dec' suffix1='_blind' \
	in2=prior_comp.vot values2='ra dec' suffix2='_prior' \
	join=1and2 fixcols=all out=$@ 

priorized_hist.png: priorized_plots.py bane_prior_xm.vot
	python $<

phoenix.png sim.png: image_plots.py 1997.fits ../MapF00E07.fits
	python $<

overlaps.png: regroup_example.py 1997.fits bane_comp.vot
	python $<

ds9.png: 1997.fits bane_comp.reg
	 ~/Software/DS9/ds9 -single 1997.fits -cmap cubehelix0 -crop 1937 800 60 60 -pan 1937 800 \
	-zoom to fit -zoom to 5.5 -scale limits -1e-3 5e-3 -region load bane_comp.reg \
	-grid yes -grid type publication -grid numerics type exterior -grid axes type exterior \
	-grid grid no -grid numerics color black -grid axes color black -colorbar off \
	-grid title no \
	-saveimage ds9.png -exit
	convert $@ -trim $@

mask.mim:
	MIMAS -depth 12 +c 17.8 -45.5 0.5 +c 17.8 -46.0 0.5 +c 18.0675096614 -45.625 0.5 +c 18.0675096614 -45.875 0.5 +c 17.5324903386 -45.625 0.5 +c 17.5324903386 -45.875 0.5 -o mask.mim

mask.reg: mask.mim
	MIMAS --mim2reg mask.mim mask.reg

mask.png: 1997.fits mask.reg
	~/Software/DS9/ds9 -single bane_rms.fits -crop 1640 1700 2870 3000 -cmap cubehelix0 \
	-zoom to fit -zoom to 0.115 -scale limits 0 4e-4 -region load mask.reg \
	-grid yes -grid type publication -grid numerics type exterior -grid axes type exterior \
	-grid grid no -grid numerics color black -grid axes color black -colorbar off \
	-grid title no \
	-saveimage mask.png -exit
	convert $@ -trim $@
FORCE: