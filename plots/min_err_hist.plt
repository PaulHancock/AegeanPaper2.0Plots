java -jar ~/Software/stilts.jar plot2plane \
	layer1=histogram in1=$1 x1="abs(b_2-b_1)/err_b" leglabel1='+C' color1='red'  barform1=filled transparency1=0.7 \
	layer2=histogram in2=$2 x2="abs(b_2-b_1)/err_b" leglabel2='-C' color2='blue' barform2=filled transparency2=0.7 \
	layer3=histogram in3=$3 x3="abs(b_2-b_1)/err_b" leglabel3='c97' color3='green' barform3=filled transparency3=0.7 \
	legend=true texttype=Latex xmin=0.05 xmax=100 ymax=1500 \
	xlog=true xlabel="b \$\Delta/\sigma\$" out="$4"