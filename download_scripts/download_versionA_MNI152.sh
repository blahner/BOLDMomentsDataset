#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="your/path/to/BOLDMomentsDataset"
dataset_path="derivatives/versionA/MNI152/prepared_data/prepared_allvoxel_pkl"
TR_folder="TRavg56789"
#create directory paths that mimic the openneuro dataset structure
mkdir -p "${LOCAL_DIR}/${dataset_path}"

#download the README file
aws s3 cp --no-sign-request \
"s3://openneuro.org/ds005165/derivatives/versionA/MNI152/prepared_data/README.txt" \
"${LOCAL_DIR}/derivatives/versionA/MNI152/prepared_data/"

for sub in {01..10}; do
    data_dir="${LOCAL_DIR}/${dataset_path}/${TR_folder}/sub-${sub}"
    mkdir -p "${data_dir}"
    aws s3 sync --no-sign-request \
    "s3://openneuro.org/ds005165/${dataset_path}/${TR_folder}/sub-${sub}/" \
    "${data_dir}/"
done