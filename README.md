# GTL_photo_matcher
set of tools for my spring 2018 special problem (main repo: https://github.com/anliec/FCSS)

## Photo matcher

Use the local Lake dataset to propose pair of same place images to the user and ask him to grade the similarity of the pair.
The list of file with the corresponding grade is then writen to a csv file.

## Dataset generator

A simple bash script that copy and resize the images for the previously generated csv file
to build the full directory structure of the dataset.

It create at the same time basic mask, to allow FCSS training to run the dataset smoothly.

## Mask generator

A more advanced mask generator. Try to mask sky and add borders.

