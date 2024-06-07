# BOLD Moments Dataset
<p align="center">
    <img src="images/BOLDMoments_mosaic.gif" width="50%" height="auto">
</p>

This GitHub repository contains starter code for the BOLD Moments dataset (BMD) as described in
the publication, ["Modeling short visual events through the BOLD Moments video fMRI dataset and metadata."](https://www.biorxiv.org/content/10.1101/2023.03.12.530887v2)

The dataset is deposited in this [OpenNeuro repository](todo).
    
BMD contains fMRI brain responses to 1,102 3 second videos for 10 subjects. Each naturalistic video
includes at least 5x human-annotated object, scene, action, and text description labels, and 
1x spoken transcription, memorability score, and memorability decay rate. The 1000-video training
set was repeated to each subject 3x and the 102-video testing set was repeated to each subject
10x for a total of 40,200 single trial responses. The dataset additionally contains structural, 
video-based functional localizer, and functional resting state scans. All data and analysis code
is available for download in this OpenNeuro repository:

### ./downloads/
These bash scripts are a template to help you download the data you want from the BMD repository.
Since the derivatives of this dataset are very large (mostly due to the 9 TR estimates per trial in version A),
you will most likely NOT want to download all the data in the repository.

We have found the quickest and easiest ways to download the data are:
 - aws s3 sync --no-sign-request (aws command line interface, https://aws.amazon.com/cli/)
 - oppeneuro-py (https://github.com/hoechenberger/openneuro-py)

We provide example scripts for both methods. The "download" tab in the OpenNeuro repository contains additional methods to donwload the dataset.

See this [GitHub repository](https://github.com/pbw-Berwin/M4-pretrained) for download and inference instructions for the M4 TSM ResNet50 model.

### ./examples/
These scripts help users familiarize themselves with different versions of the dataset and different analyses
you can do with it. The files in './examples/beta_preparation' give example code used in version B for fMRIPrep preprocessing, GLM estimation, and beta preparation. The paths are relative to the dataset repository paths. The code used for analyses in 
the manuscript is kept in their appropriate locations in the OpenNeuro repository under ./derivatives/versionX/scripts. 

### Third party imports
The scripts make heavy use of the following third party imports (among others):
- nilearn
- nibabel
- scipy
- hcp_utils
- numpy

### Citation
If you use this dataset, please cite:

Lahner et al. Modeling short visual events through the BOLD Moments video fMRI dataset and metadata. Nature Communications, (2024).