java -jar ~/Software/stilts.jar plot2plane \
	layer1=mark in1=$1 x1="abs(ra-RAJ2000)/err_ra" y1="abs(dec-DEJ2000)/err_dec" leglabel1='+C' color1='red' xmin=0.01 xmax=1000000 ymin=0.01 ymax=1000000 \
	layer2=mark in2=$2 x2="abs(ra-RAJ2000)/err_ra*100" y2="abs(dec-DEJ2000)/err_dec*100" leglabel2='-C *100' color2='blue' \
	layer3=mark in3=$3 x3="abs(ra-RAJ2000)/err_ra*10000" y3="abs(dec-DEJ2000)/err_dec*10000" leglabel3='c97*10000' color3='green' \
	legend=true texttype=Latex \
	xlog=true ylog=true xlabel="RA \$\Delta/\sigma\$" ylabel="DEC  \$\Delta/\sigma\$" out="$4"