set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR=/data/vision/oliva/scratch/datasets/BOLDMomentsDataset_tmp

dataset_files=("dataset_description.json"
    "participants.json"
    "participants.tsv"
    "README"
    "CHANGES"
    "task-train_events.json"
    "task-test_events.json"
    "task-localizer_events.json")

mkdir ${LOCAL_DIR}/Nifti/
for f in "${dataset_files[@]}"; do
    aws s3 cp --no-sign-request s3://openneuro.org/ds005032/${f} \
    ${LOCAL_DIR}/Nifti/
done

for sub in {01..10}; do
    mkdir ${LOCAL_DIR}/Nifti/sub-${sub}
    aws s3 sync --no-sign-request s3://openneuro.org/ds005032/sub-${sub}/ \
    ${LOCAL_DIR}/Nifti/sub-${sub}
done