#!/bin/bash

cat "grazing_EAperIsotopeInput.txt" | ./grazing_9

filename=*.dat
filename_arr=($filename)
firstfile=${filename_arr[0]}

echo $firstfile

rm *.dat
