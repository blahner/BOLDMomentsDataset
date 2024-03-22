set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR=/data/vision/oliva/scratch/blahner/BMD_tmp
mkdir ${LOCAL_DIR}
mkdir ${LOCAL_DIR}/derivatives
mkdir ${LOCAL_DIR}/derivatives/stimuli_metadata
mkdir ${LOCAL_DIR}/derivatives/stimuli_metadata/mp4_h264

aws s3 sync --no-sign-request s3://openneuro.org/ds005032/derivatives/stimuli_metadata/mp4_h264 \
    ${LOCAL_DIR}/derivatives/stimuli_metadata/mp4_h264/
dataset_files=("annotations.json")

for f in "${dataset_files[@]}"; do
    aws s3 cp --no-sign-request s3://openneuro.org/ds005032/derivatives/stimuli_metadata/${f} \
    ${LOCAL_DIR}/stimuli_metadata/
done