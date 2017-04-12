java -jar ~/Software/stilts.jar plot2plane \
	layer1=mark in1=$1 x1="peak_flux_1" y1="abs(peak_flux_2-peak_flux_1)/err_peak_flux" leglabel1='+C' color1='red' \
	layer2=mark in2=$2 x2="peak_flux_1*100" y2="abs(peak_flux_2-peak_flux_1)/err_peak_flux" leglabel2='-C *100' color2='blue' \
	layer3=mark in3=$3 x3="peak_flux_1*10000" y3="abs(peak_flux_2-peak_flux_1)/err_peak_flux" leglabel3='c97 *10000' color3='green' \
	legend=true \
	xlog=true ylog=true xlabel="True Flux (Jy)" ylabel="Difference/error" title="Using C" out="$4"