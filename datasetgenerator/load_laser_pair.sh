#!/bin/bash

src_file="/cs-share/pradalier/lake/pairs/image_pairs.csv"
dst_file="./pair.csv"

if [[ -f "$dst_file" ]]; then
    rm "$dst_file"
fi

while IFS=',' read -r dir1 img1 dir2 img2
do
    sd1=$(( img1 / 1000 ))
    f1=$(( img1 - (1000 * sd1) ))
    sd2=$(( img2 / 1000 ))
    f2=$(( img2 - (1000 * sd2) ))
    printf "/cs-share/pradalier/lake/VBags/%06d/%04d/%04d.jpg, /cs-share/pradalier/lake/VBags/%06d/%04d/%04d.jpg, 1\n" $dir1 $sd1 $f1 $dir2 $sd2 $f2 >> "$dst_file"
done < "$src_file"

