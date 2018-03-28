#!/bin/bash

pairs_num=$1
pair_file="negativepair.csv"

if [[ $# != "1" ]]; then
	echo "wrong call"
	exit
fi
if [ -z "${pairs_num##*[!0-9]*}" ] 2>/dev/null; then
	echo "argument must be positive integer"
	exit
fi

if [[ ! -f photolist.txt ]]; then
	echo "please generate 'photolist.txt' file first"
	exit
fi


shuf -n $((pairs_num*2)) photolist.txt > photolist_shuf.txt

i=0
first_image=""

if [[ -f "$pair_file" ]]; then
	rm "$pair_file"
fi

while read line; do
	if [[ "$first_image" == "" ]]; then
		first_image=$line
	else
		echo "$first_image, $line, -1" >> "$pair_file"
		i=$((i+1))
		first_image=""
	fi
done < photolist_shuf.txt


