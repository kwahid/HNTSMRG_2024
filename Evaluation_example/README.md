# Evaluation Example

This directory contains files and example data for evaluating the performance of segmentation models using "ground truth" and "prediction" masks for the [HNTS-MRG 2024 Challenge](https://hntsmrg24.grand-challenge.org/). The evaluation process includes the calculation of the aggregated Dice Similarity Coefficient (DSCagg) to measure the accuracy of the segmentation across a set of patients. More information on the evaluation for the challenge can be found on the [Tasks and Evaluation page of our Grand Challenge Website](https://hntsmrg24.grand-challenge.org/tasks-and-evaluation/). 

## Directory Structure

We provide some example data to run the code. The masks used as examples for the code are a subset of the [HNTS-MRG 2024 Training dataset on Zenodo](https://zenodo.org/records/11199559). You should replace the ground-truth and prediction masks with your own data. 


### Ground Truth Masks

This directory contains ground truth masks for mid-treatment imaging data (you can think of this as an evaluation for Task 2 of the challenge). These masks serve as the reference for evaluating the accuracy of predicted masks.

#### Files

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

### Prediction Masks

This directory contains "predicted" masks. In this scenario, we take the pre-RT mask as a "prediction"; we use the word prediction loosley here. These masks are used for comparison with ground truth masks to evaluate the accuracy of simply propagating registered segmentations to the next timepoint.

#### Files

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

## DSCagg_calculation.ipynb

This Jupyter Notebook, `DSCagg_calculation.ipynb`, is used to calculate the DSCagg for evaluating the accuracy of the predicted masks compared to the ground truth masks.

## Notes

- The DSCagg values range from 0 to 1, where 1 indicates perfect overlap, and 0 indicates no overlap.
- DSCagg was initially described in detail in [this paper (doi: 10.1109/EMBC48229.2022.9871907)](https://ieeexplore.ieee.org/document/9871907).

