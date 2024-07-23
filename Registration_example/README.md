# Registration Example

This directory contains code and example files for deformably registering MRI images in the context of head and neck cancer treatment using SimpleElastix. Image registration is a crucial step in aligning images from different time points or modalities to ensure accurate comparison and analysis. 

These registration scripts were used to create data for the HNTS-MRG 2024 Training and Test sets. More info on the dataset can be found on the [Dataset page of our Grand Challenge website](https://hntsmrg24.grand-challenge.org/dataset/).

## Directory Structure

### Example Data

The `example_data` folder contains pre-treatment and mid-treatment imaging data and masks for a head and neck cancer patient. It corresponds to patient ID 2 from the [Training dataset on Zenodo](https://zenodo.org/records/11199559).

- `example_data/2/preRT/2_preRT_T2.nii.gz` - Pre-treatment T2-weighted imaging data for the example patient.
- `example_data/2/preRT/2_preRT_mask.nii.gz` - Pre-treatment mask for the example patient.
- `example_data/2/midRT/2_midRT_T2.nii.gz` - Mid-treatment T2-weighted imaging data for the example patient.
- `example_data/2/midRT/2_midRT_mask.nii.gz` - Mid-treatment mask for the example patient.

### Scripts and Notebooks

- `Elastix_parameterset_23.txt` - Parameter set for the Elastix registration tool. Corresponds to [parameter set 23 from the Elastix Model Zoo](https://github.com/SuperElastix/ElastixModelZoo/tree/master/models/Par0027). 
- `Elastix_registration_example.ipynb` - Jupyter Notebook demonstrating the registration process using Elastix.
- `environment.yml` - Conda environment file to set up the necessary dependencies.

## Usage

### Setting Up the Environment

We reccomend using a fresh enviornment with only SimpleElastix installed.

**Create and activate the conda environment**:
```
conda env create -f environment.yml --name hntsmrg_env
conda activate hntsmrg_env
```

### Registration Process

#### Prepare the Images

- Ensure the pre-treatment and mid-treatment images are available in the `example_data` directory in NIfTI format.
- Place the images in the directory if not already present.

#### Run the Jupyter Notebook

- Open `Elastix_registration_example.ipynb` in Jupyter Notebook.
- Follow the instructions within the notebook to perform the registration using the Elastix tool.
- The notebook will guide you through the process of loading images, setting parameters, and executing the registration.
- It will generate a series of .txt logging files and output the registered image (`2_preRT_T2_registered.nii.gz`) and mask (`2_preRT_mask_registered.nii.gz`) in the `example_data/2/midRT` folder. 

#### Parameter File

- The registration parameters are specified in `Elastix_parameterset_23.txt`.
- Adjust the parameters if necessary to optimize the registration for your specific dataset.

### Reviewing the Output

- The registered image will be saved as specified in the Elastix parameter file.
- Use medical imaging software (e.g., [3DSlicer](https://www.slicer.org/)) to review the alignment.

### Notes

- Adjust the parameters in the `Elastix_parameterset_23.txt` file if needed to optimize the registration for your specific dataset.
- Only a rigid registration was applied for a subset of the [Training dataset on Zenodo](https://zenodo.org/records/11199559).
