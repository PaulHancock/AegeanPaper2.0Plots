#! /bin/bash

pos=(`sky2xy SimulatedImage.fits 99.638218 -64.613535`)
x=${pos[4]}
y=${pos[5]}
getfits -o sub.fits SimulatedImage.fits ${x} ${y} 100 100
getfits -o sub_bkg.fits SimulatedImage_bkg.fits ${x} ${y} 100 100
getfits -o sub_rms.fits SimulatedImage_rms.fits ${x} ${y} 100 100
