#!/bin/bash

echo " "
echo "******************************************"
echo "******************************************"
echo "*************STARTING TESTS***************"
echo "******************************************"
echo "******************************************"
echo " "

for file in ./tests/*.lox; do
    output=$(python3 lox.py "$file")
    echo "$output"
    echo "---------------------------------------"
done