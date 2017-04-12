java -jar  ~/Software/stilts.jar plot2plane \
    layer1=histogram in1=$1 x1="abs(peak_flux_2-peak_flux_1)/err_peak_flux" leglabel1='+C' color1='red' xmin=0.1 xmax=100 ymax=1500 barform1=filled transparency1=0.7 \
    layer2=histogram in2=$2 x2="abs(peak_flux_2-peak_flux_1)/err_peak_flux" leglabel2='-C' color2='blue' barform2=filled transparency2=0.7 \
    layer3=histogram in3=$3 x3="abs(peak_flux_2-peak_flux_1)/err_peak_flux" leglabel3='c97' color3='green' barform3=filled transparency3=0.7 \
	legend=true texttype=Latex \
	xlog=true xlabel="Flux \$\Delta/\sigma\$" ylabel='Number' out="$4"