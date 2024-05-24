#first install openneuro-py at https://github.com/hoechenberger/openneuro-py
pip install openneuro-py

#second log into openneuro with your personal API key
openneuro-py login

#third run download command
openneuro-py download --dataset=ds005165 --target-dir=/your/path/to/BOLDMomentsDataset --include=derivatives/stimuli_metadata