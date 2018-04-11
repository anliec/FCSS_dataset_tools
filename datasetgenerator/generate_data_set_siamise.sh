#!/bin/bash

if [[ "$#" != "2" ]] ; then
    echo "wrong number of argument"
    echo "expected call is:"
    echo "$0 output_directory validation_split"
    echo "\tvalidation_split: integer in [0, 100] representing the percentage of data used for validation"
    exit 1
fi

input_file="pair.csv"
out_dir=$1
val_split=$2
i=0


echo "creating dataset into $out_dir"

while IFS=',' read -r img1 img2 dataset
do
    # remove space
    dataset=${dataset:1}
    img2=${img2:1}
    if [[ "$dataset" != "-2" && "$dataset" != "-3" ]] ; then
        if [ ! -d "${out_dir}/train/left/${dataset}" ] ; then
            mkdir -p "${out_dir}/train/left/${dataset}"
        fi
        if [ ! -d "${out_dir}/train/right/${dataset}" ] ; then
            mkdir -p "${out_dir}/train/right/${dataset}"
        fi
        if [ ! -d "${out_dir}/test/left/${dataset}" ] ; then
            mkdir -p "${out_dir}/test/left/${dataset}"
        fi
        if [ ! -d "${out_dir}/test/right/${dataset}" ] ; then
            mkdir -p "${out_dir}/test/right/${dataset}"
        fi
        img1_file_name=${img1##*/}
        img1_file_name=${img1_file_name%.*}
        img2_file_name=${img2##*/}
        img2_file_name=${img2_file_name%.*}
        img1_date=${img1%/*/*}
        img1_date=${img1_date##*/}
        img2_date=${img2%/*/*}
        img2_date=${img2_date##*/}
        out_name="${img1_date}-${img1_file_name}_${img2_date}-${img2_file_name}"

        if (( ( RANDOM % 100 ) >= ${val_split} )); then
            val_dir="train"
        else
            val_dir="test"
        fi
        # copy and resize images (keeping aspect ratio, zero will be added at load time)
        convert "$img1" -resize 400x300 "${out_dir}/${val_dir}/left/${dataset}/${out_name}.png" &
        convert "$img2" -resize 400x300 "${out_dir}/${val_dir}/right/${dataset}/${out_name}.png" &

        if [[ $((i%10)) == "9" ]]; then
            wait
        fi
        i=$((i+1))
        
    fi
done < "$input_file"

wait
