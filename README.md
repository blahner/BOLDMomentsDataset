# BOLD Moments Dataset
<p align="center">
    <img src="images/BOLDMoments_mosaic.gif" width="50%" height="auto">
</p>

This GitHub repository contains starter code for the BOLD Moments dataset (BMD) as described in
the publication, ["BOLD Moments: modeling short visual events through a video fMRI dataset and metadata."](https://www.biorxiv.org/content/10.1101/2023.03.12.530887v2)
    
The dataset contains fMRI brain responses to 1,102 3 second videos for 10 subjects. Each 'in-the-wild' video
includes at least 5x human-annotated object, scene, action, and text description labels, and 
1x spoken transcription, memorability score, and memorability decay rate. The 1000-video training
set was repeated to each subject 3x and the 102-video testing set was repeated to each subject
10x for a total of 40,200 single trial responses. The dataset additionally contains structural, 
video-based functional localizer, and functional resting state scans. All data and analysis code
is available for download in this OpenNeuro repository:

### ./downloads/
These bash scripts are a template to help you download the data you want from the BMD repository.
Since the derivatives of this dataset are very large (mostly due to the 9 TR estimates per trial in versionA),
you will most likely NOT want to download all the data in the repository.

We have found the easiest ways to download the data are:
 - scp command through s3 buckets (see code here)
 - oppeneuro-py (https://github.com/hoechenberger/openneuro-py)

We provide example scripts for both methods. The "download" tab in the OpenNeuro repository contains additional methods to donwload the dataset.

### ./examples/
These scripts help users familiarize themselves with different versions of the dataset and different analyses
you can do with it. The paths are relative to the dataset repository paths. The code used for analyses in 
the manuscript is kept in their appropriate locations in the BMD repository under ./derivatives. 

### Third party imports
The scripts make heavy use of the following third party imports (among others):
- nilearn
- nibabel
- scipy
- hcp_utils
- numpy

### Citation
If you use this dataset, please cite:

Lahner, B., Dwivedi, K., Iamshchinina, P., Graumann, M., Lascelles, A., Roig, G., ... & Cichy, R. (2023). BOLD Moments: modeling short visual events through a video fMRI dataset and metadata. bioRxiv, 2023-03.
