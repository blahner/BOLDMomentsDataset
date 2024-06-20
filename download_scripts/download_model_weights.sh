#!/bin/bash
set -e
LOCAL_DIR="your/path/to/BOLDMomentsDataset"
mkdir -p "${LOCAL_DIR}/derivatives/Temporal_Shift_Module_DNN"

aws s3 cp --no-sign-request --recursive \
"s3://openneuro.org/ds005165/derivatives/Temporal_Shift_Module_DNN/" \
"${LOCAL_DIR}/derivatives/Temporal_Shift_Module_DNN/"