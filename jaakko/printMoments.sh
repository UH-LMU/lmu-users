#!/bin/bash

input="$1"
output="$2"

echo $input
echo $output

/Fiji.app/ImageJ-linux64 ./moments.py "$input" >& "$output"

