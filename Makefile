SIMDATA = MapF00E07.fits  MapF02E07.fits  MapF04E07.fits  MapF06E07.fits  MapF08E07.fits MapF01E07.fits  MapF03E07.fits  MapF05E07.fits  MapF07E07.fits  MapF09E07.fits SimulatedSky.vot

# Edit this to be the path of your stilts.jar file
STILTS = java -jar ~/Software/stilts.jar

Field0%_withoutC.vot : Field0%.vot MapF0%E07_withoutC_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='RAJ2000 DEJ2000' values2='ra dec' out=$@ params=30

Field0%_withC.vot : Field0%.vot MapF0%E07_withC_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='RAJ2000 DEJ2000' values2='ra dec' out=$@ params=30

Field0%_condon.vot : Field0%.vot MapF0%E07_condon_comp.fits
	$(STILTS) tmatch2 in1=$< in2=`echo $(word 2, $^)`  matcher=sky values1='RAJ2000 DEJ2000' values2='ra dec' out=$@ params=30

#This cannot go earlier as it will gobble up the previous two commands
Field00.vot Field01.vot Field02.vot Field03.vot Field04.vot Field05.vot Field06.vot Field07.vot Field08.vot Field09.vot : SimulatedSky.vot
	$(STILTS) tpipe in=$< cmd="select field==$(subst .vot,,$(subst Field0,,$@))" out=$@

MapF0%E07.fits:
	wget -O $@ https://zenodo.org/record/192096/files/$@

SimulatedSky.cat: 
	wget -O SimulatedSky.cat https://zenodo.org/record/192096/files/SimulatedSky.cat
	stilts tpipe in=SimulatedSky.cat ifmt=ASCII out=$@ ofmt=votable-binary-inline

MapF0%E07_bkg.fits MapF0%E07_rms.fits: MapF0%E07.fits
	BANE $<

MapF0%E07_withC_comp.fits : MapF0%E07.fits MapF0%E07_bkg.fits MapF0%E07_rms.fits
	aegean --autoload $< --table $(subst _comp,,$@)

MapF0%E07_withoutC_comp.fits : MapF0%E07.fits MapF0%E07_bkg.fits MapF0%E07_rms.fits
	aegean --autoload $< --table $(subst _comp,,$@) --nocov

MapF0%E07_condon_comp.fits : MapF0%E07.fits MapF0%E07_bkg.fits MapF0%E07_rms.fits
	aegean --autoload $< --table $(subst _comp,,$@) --nocov --condon

All_fields_withoutC.fits : Field00_withoutC.vot  Field02_withoutC.vot  Field04_withoutC.vot  Field06_withoutC.vot  Field08_withoutC.vot Field01_withoutC.vot  Field03_withoutC.vot  Field05_withoutC.vot  Field07_withoutC.vot  Field09_withoutC.vot
	$(STILTS) tcatn nin=10 in1=Field00_withoutC.vot \
	in2=Field01_withoutC.vot in3=Field02_withoutC.vot \
	in4=Field03_withoutC.vot in5=Field04_withoutC.vot \
	in6=Field05_withoutC.vot in7=Field06_withoutC.vot \
	in8=Field07_withoutC.vot in9=Field08_withoutC.vot \
	in10=Field09_withoutC.vot out=All_fields_withoutC.fits

All_fields_withC.fits : Field00_withC.vot  Field02_withC.vot  Field04_withC.vot  Field06_withC.vot  Field08_withC.vot Field01_withC.vot  Field03_withC.vot  Field05_withC.vot  Field07_withC.vot  Field09_withC.vot
	$(STILTS) tcatn nin=10 in1=Field00_withC.vot \
	in2=Field01_withC.vot in3=Field02_withC.vot \
	in4=Field03_withC.vot in5=Field04_withC.vot \
	in6=Field05_withC.vot in7=Field06_withC.vot \
	in8=Field07_withC.vot in9=Field08_withC.vot \
	in10=Field09_withC.vot out=All_fields_withC.fits

All_fields_condon.fits : Field00_condon.vot  Field02_condon.vot  Field04_condon.vot  Field06_condon.vot  Field08_condon.vot Field01_condon.vot  Field03_condon.vot  Field05_condon.vot  Field07_condon.vot  Field09_condon.vot 
	$(STILTS) tcatn nin=10 in1=Field00_condon.vot \
	in2=Field01_condon.vot in3=Field02_condon.vot \
	in4=Field03_condon.vot in5=Field04_condon.vot \
	in6=Field05_condon.vot in7=Field06_condon.vot \
	in8=Field07_condon.vot in9=Field08_condon.vot \
	in10=Field09_condon.vot out=All_fields_condon.fits


# Making a bunch of plots
.PHONY: plots
plots: All_fields_withC.fits All_fields_withoutC.fits All_fields_condon.fits
	$(MAKE) -C plots all

.PHONY: pnx
pnx: 
	$(MAKE) -C phoenix all

.PHONY: psf
psf:
	$(MAKE) -C psf all

.PHONY: catalogues
catalogues : MapF00E07_withC_comp.fits  MapF02E07_withC_comp.fits  MapF04E07_withC_comp.fits  MapF06E07_withC_comp.fits  MapF08E07_withC_comp.fits MapF01E07_withC_comp.fits  MapF03E07_withC_comp.fits  MapF05E07_withC_comp.fits  MapF07E07_withC_comp.fits  MapF09E07_withC_comp.fits MapF00E07_withoutC_comp.fits  MapF02E07_withoutC_comp.fits  MapF04E07_withoutC_comp.fits  MapF06E07_withoutC_comp.fits  MapF08E07_withoutC_comp.fits MapF01E07_withoutC_comp.fits  MapF03E07_withoutC_comp.fits  MapF05E07_withoutC_comp.fits  MapF07E07_withoutC_comp.fits  MapF09E07_withoutC_comp.fits MapF00E07_condon_comp.fits  MapF02E07_condon_comp.fits  MapF04E07_condon_comp.fits  MapF06E07_condon_comp.fits  MapF08E07_condon_comp.fits MapF01E07_condon_comp.fits  MapF03E07_condon_comp.fits  MapF05E07_condon_comp.fits  MapF07E07_condon_comp.fits  MapF09E07_condon_comp.fits

.PHONY: fields
fields : Field00.vot Field01.vot Field02.vot Field03.vot Field04.vot Field05.vot Field06.vot Field07.vot Field08.vot Field09.vot


FORCE:
