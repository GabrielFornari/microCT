#!/bin/bash

currentAngle=0
targetFolder=$1
folderOutput=$2
anglePace=$3

cd $targetFolder
mkdir $folderOutput

echo "Starting simulation..."
while [ "$currentAngle" -lt 360 ]
do
   oldAngle=$currentAngle
   
   xrmc input.dat >/dev/null
   
   imgName="img_$currentAngle.dat"
   mv image.dat $folderOutput/$imgName

   currentAngle=$((currentAngle+anglePace))
   echo -ne "Progress: "$((100*currentAngle/360))" %\r"

   sed -i 's/RotateAll 0 0 0 0 0 1 '$oldAngle'/RotateAll 0 0 0 0 0 1 '$currentAngle'/g' quadric.dat
done

sed -i 's/RotateAll 0 0 0 0 0 1 '$currentAngle'/RotateAll 0 0 0 0 0 1 0/g' quadric.dat

echo -ne "\n"
echo "Simulation complete."

echo "Moving folder..."

mv $folderOutput ../$folderOutput
cd ..

echo "Done."
