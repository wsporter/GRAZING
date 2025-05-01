#!/bin/bash

cat "grazing_defaultInput.txt" | ./grazing_9

mv *.dat Converter/

cd Converter

filename=*.dat
filename_arr=($filename)
firstfile=${filename_arr[0]}

echo $firstfile | python3 Output_Conversor.py

rm *.dat
