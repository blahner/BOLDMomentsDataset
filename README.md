# BOLD Moments Dataset
![mosaic gif of example BMD videos][images/BOLDMoments_mosaic.gif]

This GitHub repository contains starter code for the BOLD Moments dataset (BMD) as described in
the publication, ["BOLD Moments: modeling short visual events through a video fMRI dataset and metadata."]
(https://www.biorxiv.org/content/10.1101/2023.03.12.530887v2)
    
The dataset contains fMRI brain responses to 1,102 3 second videos for 10 subjects. Each video
includes at least 5x human-annotated object, scene, action, and text description labels, and 
1x spoken transcription, memorability score, and memorability decay rate. The 1000-video training
set was repeated to each subject 3x and the 102-video testing set was repeated to each subject
10x for a total of 40,200 single trial responses. The dataset additionally contains structural, 
video-based functional localizer, and functional resting state scans. All data and analysis code
is available for download in this OpenNeuro repository:

### ./downloads/
These bash scripts are a template to help you download the data you want from the BMD repository.

### ./examples/
These scripts help users familiarize themselves with different versions of the dataset and different analyses
you can do with it. The paths are relative to the dataset repository paths. The code used for analyses in 
the manuscript is kept in their appropriate locations in the BMD repository under ./derivatives. 

### third party imports
The scripts make heavy use of following third party imports (among others):
- nilearn
- nibabel
- scipy
- hcp_utils
- numpy

### citation
If you use this dataset, please cite:

@article{lahner2023bold,
  title={BOLD Moments: modeling short visual events through a video fMRI dataset and metadata},
  author={Lahner, Benjamin and Dwivedi, Kshitij and Iamshchinina, Polina and Graumann, Monika and Lascelles, Alex and Roig, Gemma and Gifford, Alessandro Thomas and Pan, Bowen and Jin, SouYoung and Ratan Murty, N Apurva and others},
  journal={bioRxiv},
  pages={2023--03},
  year={2023},
  publisher={Cold Spring Harbor Laboratory}
}
