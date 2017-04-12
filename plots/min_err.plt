java -jar ~/Software/stilts.jar plot2plane \
	layer1=mark in1=$1 x1="abs(a_2-a_1)/err_a" y1="abs(b_2-b_1)/err_b" leglabel1='+C' color1='red' \
	layer2=mark in2=$2 x2="abs(a_2-a_1)/err_a" y2="abs(b_2-b_1)/err_b" leglabel2='-C' color2='blue' \
	legend=true texttype=Latex xmin=0.01 xmax=10000 ymin=0.01 ymax=10000 \
	xlog=true ylog=true xlabel="a \$\Delta/\sigma\$" ylabel="b  \$\Delta/\sigma\$" out="$4"