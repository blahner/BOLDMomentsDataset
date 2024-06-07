#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/data/vision/oliva/scratch/datasets/BOLDMomentsDataset_tmp"

#put the un-preprocessed dataset in its own folder
mkdir -p "${LOCAL_DIR}/Nifti"

#download directory files
dataset_files=("participants.json"
    "dataset_description.json"
    "participants.tsv"
    "README"
    "CHANGES"
    "task-train_events.json"
    "task-test_events.json"
    "task-localizer_events.json")

for file in "${dataset_files[@]}"; do
    aws s3 cp --no-sign-request \
    "s3://openneuro.org/ds005165/${file}" \
    "${LOCAL_DIR}/Nifti/"
done

#download subject folders
for sub in {01..10}; do
    sub_dir="${LOCAL_DIR}/Nifti/sub-${sub}"
    mkdir -p "${sub_dir}"
    aws s3 cp --no-sign-request --recursive \
    "s3://openneuro.org/ds005165/sub-${sub}/" \
    "${sub_dir}/"
done