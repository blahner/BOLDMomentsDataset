#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/data/vision/oliva/scratch/datasets/BOLDMomentsDataset_tmp"
dataset_path="derivatives/versionB/fsLR32k/GLM"
#create directory paths that mimic the openneuro dataset structure
mkdir -p "${LOCAL_DIR}/${dataset_path}"

#download the README file
aws s3 cp --no-sign-request \
"s3://openneuro.org/ds005165/derivatives/versionB/fsLR32k/README.txt" \
"${LOCAL_DIR}/derivatives/versionB/fsLR32k/"

for sub in {01..10}; do
    data_dir="${LOCAL_DIR}/${dataset_path}/sub-${sub}"
    mkdir -p "${data_dir}"
    aws s3 sync --no-sign-request \
    "s3://openneuro.org/ds005165/${dataset_path}/sub-${sub}/" \
    "${data_dir}/"
done