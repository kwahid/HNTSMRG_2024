# Evaluation Example

This directory contains the necessary files and examples for evaluating the performance of segmentation models using ground truth and prediction masks for head and neck cancer patients. The evaluation process includes the calculation of the Dice Similarity Coefficient (DSC) to measure the accuracy of the segmentation.

## Directory Structure

### Ground Truth Masks

This directory contains ground truth masks for mid-treatment imaging data. These masks serve as the reference standard for evaluating the accuracy of predicted masks.

#### File Structure

- `8_midRT_mask.nii.gz`
- `77_midRT_mask.nii.gz`
- `78_midRT_mask.nii.gz`
- `80_midRT_mask.nii.gz`
- `81_midRT_mask.nii.gz`
- `84_midRT_mask.nii.gz`
- `86_midRT_mask.nii.gz`
- `88_midRT_mask.nii.gz`
- `90_midRT_mask.nii.gz`
- `91_midRT_mask.nii.gz`
- `93_midRT_mask.nii.gz`
- `94_midRT_mask.nii.gz`
- `95_midRT_mask.nii.gz`
- `96_midRT_mask.nii.gz`
- `99_midRT_mask.nii.gz`

#### Description

Each NIfTI file in this directory corresponds to a specific patient and represents the ground truth segmentation of relevant anatomical structures as observed in mid-treatment imaging. These masks are crucial for assessing the performance of prediction models in accurately identifying and segmenting structures during the course of treatment.

#### Usage

These ground truth masks are intended to be used for:
- Validating and benchmarking segmentation algorithms.
- Comparing pre-treatment and mid-treatment anatomical changes.
- Enhancing the accuracy of radiation therapy planning through improved model predictions.

#### File Format

The masks are stored in NIfTI format, which is widely used in medical imaging due to its ability to store multidimensional data along with metadata. Each file contains:
- Voxel-wise segmentation data.
- Relevant header information for proper spatial orientation.

#### Notes

- Ensure that the NIfTI files are correctly registered to the corresponding imaging data.
- When using these masks, please cite the original source or dataset if applicable.

---

### Prediction Masks

This directory contains predicted masks for pre-treatment imaging data. These masks are used for comparison with ground truth masks to evaluate the accuracy of predictive models.

#### File Structure

- `8_preRT_mask_registered.nii.gz`
- `77_preRT_mask_registered.nii.gz`
- `78_preRT_mask_registered.nii.gz`
- `80_preRT_mask_registered.nii.gz`
- `81_preRT_mask_registered.nii.gz`
- `84_preRT_mask_registered.nii.gz`
- `86_preRT_mask_registered.nii.gz`
- `88_preRT_mask_registered.nii.gz`
- `90_preRT_mask_registered.nii.gz`
- `91_preRT_mask_registered.nii.gz`
- `93_preRT_mask_registered.nii.gz`
- `94_preRT_mask_registered.nii.gz`
- `95_preRT_mask_registered.nii.gz`
- `96_preRT_mask_registered.nii.gz`
- `99_preRT_mask_registered.nii.gz`

#### Description

Each NIfTI file in this directory corresponds to a specific patient and represents the predicted segmentation of relevant anatomical structures as observed in pre-treatment imaging. These predictions are compared against mid-treatment ground truth masks to assess the performance and reliability of the segmentation models.

#### Usage

These prediction masks are intended to be used for:
- Evaluating the accuracy of segmentation models against ground truth data.
- Studying pre-treatment anatomical structures for better treatment planning.
- Research and development of improved predictive models for radiation oncology.

#### File Format

The masks are stored in NIfTI format, which is widely used in medical imaging due to its ability to store multidimensional data along with metadata. Each file contains:
- Voxel-wise segmentation data.
- Relevant header information for proper spatial orientation.

#### Notes

- Ensure that the NIfTI files are correctly registered to the corresponding imaging data.
- When using these masks, please cite the original source or dataset if applicable.

---

### DSCagg_calculation.ipynb

This Jupyter Notebook, `DSCagg_calculation.ipynb`, is used to calculate the Dice Similarity Coefficient (DSC) for evaluating the accuracy of the predicted masks compared to the ground truth masks.

#### Description

The Dice Similarity Coefficient (DSC) is a statistical tool used to measure the similarity between two sets of data. In this context, it is used to compare the overlap between the predicted segmentation masks and the ground truth segmentation masks.

#### Usage

1. Ensure that the predicted masks and ground truth masks are correctly registered and aligned.
2. Load the `DSCagg_calculation.ipynb` notebook.
3. Follow the instructions within the notebook to calculate the DSC for each pair of masks.

#### Notes

- The DSC values range from 0 to 1, where 1 indicates perfect overlap and 0 indicates no overlap.
- Use the calculated DSC values to evaluate and improve the segmentation models.

---

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that your contributions adhere to the guidelines and standards of the project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- We acknowledge the contributions of all researchers and institutions involved in the creation and maintenance of this dataset.
- Please cite the original source or dataset when using these masks in your research.
