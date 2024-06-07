set -e
LOCAL_DIR="/data/vision/oliva/scratch/datasets/BOLDMomentsDataset_tmp/derivatives"
mkdir -p "${LOCAL_DIR}/Temporal_Shift_Module_DNN"

aws s3 cp --no-sign-request --recursive \
"s3://openneuro.org/ds005165/derivatives/Temporal_Shift_Module_DNN/" \
"${LOCAL_DIR}/Temporal_Shift_Module_DNN/"