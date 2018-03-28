#!/bin/bash

if [[ "$#" != "1" ]] ; then
    echo "wrong number of argument"
    echo "expected call is:"
    echo "$0 output_directory"
    exit 1
fi

input_file="pair.csv"
out_dir=$1
i=0


echo "creating dataset into $out_dir"

while IFS=',' read -r img1 img2 dataset
do
    # remove space
    dataset=${dataset:1}
    img2=${img2:1}
    if [[ "$dataset" != "-0" ]] ; then
        if [ ! -d "${out_dir}/${dataset}" ] ; then
            mkdir "${out_dir}/${dataset}"
        fi
        img1_file_name=${img1##*/}
        img1_file_name=${img1_file_name%.*}
        img2_file_name=${img2##*/}
        img2_file_name=${img2_file_name%.*}
        img1_date=${img1%/*/*}
        img1_date=${img1_date##*/}
        img2_date=${img2%/*/*}
        img2_date=${img2_date##*/}
        dir_name="${img1_date}-${img1_file_name}_${img2_date}-${img2_file_name}"

        if [ ! -d "${out_dir}/${dataset}/${dir_name}" ] ; then
            mkdir "${out_dir}/${dataset}/${dir_name}"

            # copy and resize images (keeping aspect ratio, zero will be added at load time)
            convert "$img1" -resize 400x300 "${out_dir}/${dataset}/${dir_name}/image1.png" &
            convert "$img2" -resize 400x300 "${out_dir}/${dataset}/${dir_name}/image2.png" &

            # create empty masks
            # convert -resize 340x240\! xc:white -bordercolor Black -border 30 "${out_dir}/${dataset}/${dir_name}/mask1.png"
            # convert -resize 340x240\! xc:white -bordercolor Black -border 30 "${out_dir}/${dataset}/${dir_name}/mask2.png"

            echo "Image1,Image2
            $img1,$img2" > "${out_dir}/${dataset}/${dir_name}/pair.txt"
            if [[ $((i%10)) == "9" ]]; then
                wait
            fi
            i=$((i+1))
        else
            echo "directory with name: $dir_name already exist"
        fi
    	fi
done < "$input_file"

wait
