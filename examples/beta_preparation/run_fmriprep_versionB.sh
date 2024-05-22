set -e
DATASET_ROOT="/your/path/to/BOLDMomentsDataset"
TMP="/your/path/to/tmp_directory"
WORK="$TMP/tmp/BMD-workdir"
FMRIPREP_VERSION="23.2.0"
USERNAME=blahner

#to deal with permission issues that can arise when creating folders in docker
su $USERNAME -c "mkdir -p $DATASET_ROOT/derivatives/versionB"
su $USERNAME -c "mkdir -p $WORK"

nthreads=12
ncpus=24
docker pull nipreps/fmriprep:${FMRIPREP_VERSION}

for subj in {01..10}; do
    echo "Starting fMRIPrep for sub-${subj}"
    docker run \
    #--user XXXXX:XXXXX \ a user and group id to set docker permissions
    -it --rm \
    -v $DATASET_ROOT/Nifti:/data:ro \
    -v $DATASET_ROOT/derivatives/versionD:/out \
    -v $WORK:/work \
    -v $FREESURFER_HOME/license.txt:/opt/freesurfer_license/license.txt \
    \
    nipreps/fmriprep:${FMRIPREP_VERSION} \
    /data /out \
    --skip_bids_validation \
    participant --participant-label ${subj} \
    --output-space anat fsaverage fsnative MNI152NLin2009cAsym \
    --fs-license-file /opt/freesurfer_license/license.txt \
    --cifti-output 91k \
    --bold2t1w-dof 12 \
    --slice-time-ref 0 \
    --nthreads $nthreads \
    --n-cpus $ncpus \
    --stop-on-first-crash \
    -w /work
    echo "Deleting the large tmp files from subject ${subj}"
    rm -r $WORK/fmriprep_23_2_wf/sub_${subj}_wf/
done
echo "Finished fMRIPrep for all subjects in the loop"
