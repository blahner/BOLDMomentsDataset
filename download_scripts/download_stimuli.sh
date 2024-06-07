#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/data/vision/oliva/scratch/datasets/BOLDMomentsDataset_tmp"

#create directory paths that mimic the openneuro dataset structure
mkdir -p "${LOCAL_DIR}/derivatives/stimuli_metadata"

#download the files
dataset_files=(
    "README.txt"
    "annotations.json"
    "llm_frame_annotations.json"
    "annotations_fieldnames.json"
    "frames.zip"
    )

for file in "${dataset_files[@]}"; do
    aws s3 cp --no-sign-request \
    "s3://openneuro.org/ds005165/derivatives/stimuli_metadata/${file}" \
    "${LOCAL_DIR}/derivatives/stimuli_metadata/"
done

#download the folders
dataset_folders=(
    "mp4_h264"
    "stimuli"
    "frames_middle"
    "ME_feats_matlab"
)
for folder in "${dataset_folders[@]}"; do
    mkdir -p "${LOCAL_DIR}/derivatives/stimuli_metadata/${folder}"

    aws s3 cp --no-sign-request --recursive \
    "s3://openneuro.org/ds005165/derivatives/stimuli_metadata/${folder}/" \
    "${LOCAL_DIR}/derivatives/stimuli_metadata/${folder}/"
done

