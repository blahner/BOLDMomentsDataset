import numpy as np
import scipy
import time
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import pickle
import os
import argparse
from glmsingle.glmsingle import GLM_single
import nibabel as nib
import subprocess

#compute glm using glmsingle
# https://github.com/cvnlab/GLMsingle

def interpolate_ts(fmri, tr_acq, tr_resamp):
    #interopolate the fmri time series. Can be either 2D (surface x time) or 4D (volume x time) array.
    #number of scans (time) has to be the last dimension
    numscans_acq = fmri.shape[-1]
    secsperrun = numscans_acq*tr_acq #time in seconds of the run
    numscans_resamp = int(secsperrun/tr_resamp)

    x = np.linspace(0, numscans_acq, num=numscans_acq, endpoint=True)
    f = scipy.interpolate.interp1d(x, fmri)
    x_new = np.linspace(0, numscans_acq, num=numscans_resamp, endpoint=True)

    fmri_interp = f(x_new)
    return fmri_interp

def main(args):
    subject = f"sub-{int(args.subject):02}"
    session = "ses-01"
    if args.verbose:
        print("Running GLMsingle on the localizer task for subject {}".format(subject))

    TR = 1.75 #acquisition TR
    TR_resamp = 1 # resample time series to be locked to stimulus onset
    stimDur = 18 #in seconds
    dummy_offset = 0 #offset of start. in seconds

    if args.verbose:
        print("#" * 20)
        print("Starting GLMsingle on main experimental data for subject {} session {}".format(subject, session))
        print("#" * 20)
    sub_func_root = os.path.join(args.dataset_root, "derivatives", "versionB", "fmriprep", subject, session, "func")
    tmp_root = os.path.join(args.dataset_root, "derivatives", "versionB","tmp") #to temporarily store smoothed cifti files
    data = []
    design = []
    numruns = 5
    task = 'localizer'
    cols = ['trial_type','onset']
    events_run = []     
    ##Load eventts and data for each run
    ses_conds = [] #keep track of the unique conditions shown in this session over all runs

    for count, run in enumerate(range(1,numruns+1)):
        if args.verbose:
            print(f"task {task} run {run}")

        input_cifti_path=os.path.join(sub_func_root, f"{subject}_{session}_task-{task}_run-{run}_space-fsLR_den-91k_bold.dtseries.nii")
        surface_kernel=9 #make sure this is fwhm by using the -fwhm flag
        volume_kernel=9
        direction='COLUMN' #because it is .dtseries formal
        cifti_output=os.path.join(tmp_root, f"{subject}_{session}_task-{task}_run-{run}_space-fsLR_den-91k_bold_smooth-{surface_kernel}.dtseries.nii")
        left_surface=os.path.join(args.templateflow_root,"tpl-fsLR","tpl-fsLR_den-32k_hemi-L_midthickness.surf.gii")
        right_surface=os.path.join(args.templateflow_root,"tpl-fsLR","tpl-fsLR_den-32k_hemi-R_midthickness.surf.gii")

        #this requires you to download HCP workbench command
        cmd = f"wb_command -cifti-smoothing -fwhm \
            {input_cifti_path} \
            {surface_kernel} \
            {volume_kernel} \
            {direction} \
            {cifti_output} \
            -left-surface {left_surface} \
            -right-surface {right_surface}"
        if not os.path.isfile(cifti_output):
            if args.verbose:
                print(f"Smoothing cifti run {run}")
            if not os.path.exists(tmp_root):
                os.makedirs(tmp_root)
            subprocess.run(cmd, shell=True, check=True)
        else:
            if args.verbose:
                print("This smoothed cifti file aready exists. Loading it now.")
        
        cifti_ts = nib.load(cifti_output)
        cifti_data = cifti_ts.get_fdata()

        #interpolate time series
        fmri_interp = interpolate_ts(cifti_data.T, TR, TR_resamp)
        numscans_interp = fmri_interp.shape[1]
        data.append(fmri_interp)

        #load events
        events_tmp = {col: [] for col in cols}  
        tmp = pd.read_table(os.path.join(args.dataset_root, "Nifti", subject, session, "func", f"{subject}_{session}_task-{task}_run-{run}_events.tsv"))
        previous_trial_type = "fix"
        for idx, tt in enumerate(tmp.loc[:,'trial_type']):
            if tt == "fix":
                previous_trial_type = tt
                continue
            elif tt != previous_trial_type: #a change in trial type that is not fixation i.e., don't include the fixation periods in GLM
                if tt not in ses_conds:
                    ses_conds.append(tt) #keep track of the unique stimuli
                onset = tmp.loc[idx,'onset']
                events_tmp['trial_type'].append(tt)
                events_tmp['onset'].append(onset + dummy_offset)
                previous_trial_type = tt
        events_run.append(events_tmp) 
    assert(len(ses_conds) == 5)

    #create the design matrix for all runs in the session
    for count, _ in enumerate(range(1,len(data)+1)):
        numscans_interp = data[count].shape[1]
        run_design = np.zeros((numscans_interp, len(ses_conds)))
        events = events_run[count]
        for c, cond in enumerate(ses_conds):
            if cond not in events['trial_type']:
                continue
            condidx = np.argwhere(np.array(events['trial_type'])==cond)[:,0]
            onsets_t = np.array(events['onset'])[condidx]
            onsets_tr = np.round(onsets_t / TR_resamp).astype(int)
            run_design[onsets_tr, c] = 1 
        design.append(run_design)
    
    #define opt for glmsingle params
    opt = dict()
    # set important fields for completeness (but these would be enabled by default)
    opt['wantlibrary'] = 1
    opt['wantglmdenoise'] = 1
    opt['wantfracridge'] = 1

    # for the purpose of this example we will keep the relevant outputs in memory
    # and also save them to the disk
    opt['wantfileoutputs'] = [0,0,0,1]
    opt['wantmemoryoutputs'] = [0,0,0,1]

    outputdir_glmsingle = os.path.join(args.dataset_root, "derivatives", "versionB", "fsLR32k", "GLM", subject, session)
    if not os.path.exists(outputdir_glmsingle):
        os.makedirs(outputdir_glmsingle)

    start_time = time.time()
    if args.verbose:
        print(f"running GLMsingle...")
    #sometimes the default 50,000 chunk length doesn't chunk into equal lengths, throwing an error when converting to array
    numvertices = data[0].shape[0]  # get shape of data for convenience
    opt['chunklen'] = int(numvertices) 

    glmsingle_obj = GLM_single(opt)
    # run GLMsingle
    glmsingle_obj.fit(
        design,
        data,
        stimDur,
        TR_resamp,
        outputdir=outputdir_glmsingle)
    elapsed_time = time.time() - start_time

    if args.verbose:
        print(
            '\telapsed time: ',
            f'{time.strftime("%H:%M:%S", time.gmtime(elapsed_time))}'
        )
    #save design matrix
    if args.verbose:
        print("saving design matrix")
    with open(os.path.join(outputdir_glmsingle, f"{subject}_{session}_conditionOrderDM.pkl"), 'wb') as f:
        pickle.dump((events_run, ses_conds), f)
    #delete tmp directory
    subprocess.run(f"rm -r {tmp_root}", shell=True, check=True)

if __name__ == '__main__':
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subject", type=int, required=True, help="The subject from 1-10 that you wish to process")
    parser.add_argument("-d", "--dataset_root", default="/your/path/to/BOLDMomentsDataset", help="The root path to the dataset directory")
    parser.add_argument("-t", "--templateflow_root", default="/your/path/to/templateflow", help="The root path to the templateflow directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose")
    args = parser.parse_args()

    main(args)