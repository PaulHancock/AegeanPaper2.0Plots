java -jar ~/Software/stilts.jar plot2plane \
	layer1=histogram in1=$1 x1="hypot(abs(ra-RAJ2000)/err_ra,abs(dec-DEJ2000)/err_dec)/sqrt(2)" leglabel1='+C' color1='red' xmin=0.1 xmax=100 ymax=2000 barform1=filled transparency1=0.7 \
	layer2=histogram in2=$2 x2="hypot(abs(ra-RAJ2000)/err_ra,abs(dec-DEJ2000)/err_dec)/sqrt(2)" leglabel2='-C' color2='blue' barform2=filled transparency2=0.7  \
	layer3=histogram in3=$3 x3="hypot(abs(ra-RAJ2000)/err_ra,abs(dec-DEJ2000)/err_dec)/sqrt(2)" leglabel3='c97' color3='green' barform3=filled transparency3=0.7  \
	legend=true texttype=Latex \
	xlog=true xlabel="Position  \$\Delta/\sigma\$" out="$4"