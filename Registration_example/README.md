# Registration Example

This directory contains examples and necessary files for demonstrating the registration process of medical images in the context of head and neck cancer treatment. Image registration is a crucial step in aligning images from different time points or modalities to ensure accurate comparison and analysis.

## Directory Structure

### Example Data

The `example_data` folder contains pre-treatment and mid-treatment imaging data and masks for a head and neck cancer patient.

- `example_data/2_preRT_T2.nii.gz` - Pre-treatment T2-weighted imaging data for the example patient.
- `example_data/2_preRT_mask.nii.gz` - Pre-treatment mask for the example patient.
- `example_data/2_midRT_T2.nii.gz` - Mid-treatment T2-weighted imaging data for the example patient.
- `example_data/2_midRT_mask.nii.gz` - Mid-treatment mask for the example patient.

### Scripts and Notebooks

- `Elastix_parameterset_23.txt` - Parameter set for the Elastix registration tool.
- `Elastix_registration_example.ipynb` - Jupyter Notebook demonstrating the registration process using Elastix.
- `environment.yml` - Conda environment file to set up the necessary dependencies.

## Description

Image registration involves aligning two or more images to a common coordinate system, which is essential for comparing anatomical changes over time or across different imaging modalities. This example demonstrates the registration of pre-treatment and mid-treatment images for a head and neck cancer patient using the Elastix registration tool.

## Usage

### Setting Up the Environment

**Create and activate the conda environment**:
   `conda env create -f environment.yml'
   'conda activate hntsmrg_env'

### Registration Process

#### Prepare the Images

- Ensure the pre-treatment and mid-treatment images are available in the `example_data` directory in NIfTI format.
- Place the images in the directory if not already present.

#### Run the Jupyter Notebook

- Open `Elastix_registration_example.ipynb` in Jupyter Notebook.
- Follow the instructions within the notebook to perform the registration using the Elastix tool.
- The notebook will guide you through the process of loading images, setting parameters, and executing the registration.

#### Parameter File

- The registration parameters are specified in `Elastix_parameterset_23.txt`.
- Adjust the parameters if necessary to optimize the registration for your specific dataset.

### Reviewing the Output

- The registered image will be saved as specified in the Elastix parameter file.
- Use medical imaging software to review the alignment.

### File Format

The images and masks are stored in NIfTI format, which is widely used in medical imaging due to its ability to store multidimensional data along with metadata. Each file contains:
- Voxel-wise imaging data.
- Relevant header information for proper spatial orientation.

### Notes

- Ensure that the images are correctly oriented and scaled before running the registration.
- Adjust the parameters in the `Elastix_parameterset_23.txt` file if needed to optimize the registration for your specific dataset.
- When using these images and scripts, please cite the original source or dataset if applicable.

### Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that your contributions adhere to the guidelines and standards of the project.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments

- We acknowledge the contributions of all researchers and institutions involved in the creation and maintenance of this dataset.
- Please cite the original source or dataset when using these images and scripts in your research.
