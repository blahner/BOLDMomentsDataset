import os
import numpy as np
import argparse
import pickle

def main(args):
    fmri_path = os.path.join(args.dataset_root,"derivatives", "versionB", "fsLR32k","GLM")

    subject = f"sub-{int(args.subject):02}"
    print(f"starting {subject}")
    betas_tmp = {f"vid{stim:04}": [] for stim in range(1,1103)}
    beta_type = "TYPED_FITHRF_GLMDENOISE_RR"
    #load fMRI data from that subject and run
    for ses in range(2,6):
        print(f"loading session {ses}")
        session = f"ses-{ses:02}"

        fmri_data_wb = np.load(os.path.join(fmri_path, subject, session, f"{beta_type}.npy"), allow_pickle=True).item()
        fmri_data_wb = fmri_data_wb['betasmd'].squeeze() #squeezed to shape numvertices x numtrials
        fmri_data_wb = fmri_data_wb.T #transpose to shape numtrials x numvertices, more representative of the samples x features format

        with open(os.path.join(fmri_path, subject, session, f"{subject}_{session}_conditionOrderDM.pkl"), 'rb') as f:
            events_run, _ = pickle.load(f)

        stims = []
        for event in events_run:
            stims.extend(event['trial_type'])
        
        stim_idx_train = []
        stim_idx_test = []
        for idx, stim in enumerate(stims):
            if int(stim.split('vid')[-1]) <= 1000:
                stim_idx_train.append(idx)
            elif int(stim.split('vid')[-1]) >= 1001:
                stim_idx_test.append(idx)
            
        #zscore the test and train data separately
        fmri_data_wb_train = fmri_data_wb[stim_idx_train, :]
        fmri_data_wb_test = fmri_data_wb[stim_idx_test, :]

        #normalize the test and train betas by the train statistics
        train_mean = np.mean(fmri_data_wb_train, axis=0)
        train_std = np.std(fmri_data_wb_train, axis=0, ddof=1)

        fmri_data_wb_train_normalized = (fmri_data_wb_train - train_mean) / train_std
        fmri_data_wb_test_normalized = (fmri_data_wb_test - train_mean) / train_std

        train_count = 0
        test_count = 0
        for stim in stims:
            if int(stim.split('vid')[-1]) <= 1000:
                betas_tmp[stim].append(fmri_data_wb_train_normalized[train_count, :]) #collects all normalized responses per stimulus
                train_count += 1
            elif int(stim.split('vid')[-1]) >= 1001:
                betas_tmp[stim].append(fmri_data_wb_test_normalized[test_count, :]) #collects all normalized responses per stimulus
                test_count += 1
        assert(test_count == 255)
        assert(train_count == 750)

    stimorder_train = [f"vid{stim:04}" for stim in range(1,1001)]
    stimorder_test = [f"vid{stim:04}" for stim in range(1001,1103)]
    
    numvertices = 91282
    betas_train = np.zeros((1000, 3, numvertices))
    betas_train.fill(np.nan)
    betas_test = np.zeros((102, 10, numvertices))
    betas_test.fill(np.nan)
    for stimcount, b in enumerate(stimorder_train):
        value = betas_tmp[b]
        for repcount, v in enumerate(value): #loop over reps
            betas_train[stimcount, repcount, :] = np.array(v) #sorts the responses into an array. separate training and testing array
    for stimcount, b in enumerate(stimorder_test):
        value = betas_tmp[b]
        for repcount, v in enumerate(value): #loop over reps
            betas_test[stimcount, repcount, :] = np.array(v) #sorts the responses into an array. separate training and testing array

    #save betas
    save_root = os.path.join(fmri_path, f"{subject}", "prepared_betas")
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    print(f"saving {subject} train betas")
    with open(os.path.join(save_root, f"{subject}_organized_betas_task-train_normalized.pkl"), 'wb') as f:
        pickle.dump((betas_train,stimorder_train), f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"saving {subject} test betas")
    with open(os.path.join(save_root, f"{subject}_organized_betas_task-test_normalized.pkl"), 'wb') as f:
        pickle.dump((betas_test,stimorder_test), f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subject", type=int, required=True, help="The subject from 1-10 that you wish to process")
    parser.add_argument("-d", "--dataset_root", default="/your/path/to/BOLDMomentsDataset", help="The root path to the dataset directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose")
    args = parser.parse_args()

    main(args)