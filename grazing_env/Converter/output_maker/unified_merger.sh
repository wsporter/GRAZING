#!/bin/bash

filename=*.txt
filename_arr=($filename)

for i in ${filename_arr[@]}
do
    echo $i
    if [ $i != "output.txt" ]; then
        echo $i | python3 unified_merger.py
    fi
done
            
