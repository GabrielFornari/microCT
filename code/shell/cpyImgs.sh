#!/bin/bash

imgInput=${1%.tif}
anglePace=$2

mkdir $imgInput"_"$anglePace

currentAngle=0
iAngle=0
while [ "$currentAngle" -lt 360 ]
do
   imgName=$imgInput"_$(printf %04d $iAngle).tif"
   cp $imgInput".tif" $imgInput"_"$anglePace/$imgName

   currentAngle=$((currentAngle+anglePace))
   iAngle=$((iAngle+1))
done
