# **Example Algorithm Docker Container Images for HNTS-MRG 2024 Challenge**

**Authors:** Kareem A. Wahid (<kawahid@mdanderson.org>), Cem Dede (<cdede@mdanderson.org>).

**Note:** We would like to thank the authors of the [MIDOG](https://github.com/DeepMicroscopy/MIDOG_reference_docker), [HaN-Seg](https://github.com/gasperpodobnik/HanSeg2023Algorithm?tab=readme-ov-file#export), and [SegRap](https://github.com/HiLab-git/SegRap2023/tree/main?tab=readme-ov-file) challenges for their reference documentation on which this tutorial is based.

These files serve as templates for preparing algorithm Docker container images for the [HNTS-MRG 2024 Challenge](https://hntsmrg24.grand-challenge.org/). They include scripts and path definitions necessary to run your algorithms on the grand-challenge.org platform. To better understand how algorithms on grand-challenge.org work, you may want to read the blog posts on how to [create an algorithm](https://grand-challenge.org/documentation/create-your-own-algorithm/).

We have also recorded a series of videos that walk you through the first six sections (insert link here) and submitting an algorithm on Grand-Challenge.org (insert link here).

## **Table of Contents**

1. [Prerequisites](#1-prerequisites)
2. [Example Structure Overview](#2-example-structure-overview)
3. [Embedding an Algorithm into a Docker Container Image](#3-embedding-an-algorithm-into-a-docker-container-image)
4. [Building your Docker Container Image](#4-building-your-docker-container-image)
5. [Testing your Docker Container Image](#5-testing-your-docker-container-image)
6. [Saving your Docker Container Image as a Zip File](#6-saving-your-docker-container-image-as-a-zip-file)
7. [Submitting an Algorithm (Zipped Docker Container Image) on Grand-Challenge.org](#7-submitting-an-algorithm-zipped-docker-container-image-on-grand-challengeorg)


## **1\. Prerequisites**

**Recommendations for Windows Users:**

- As per the [Grand Challenge documentation](https://grand-challenge.org/documentation/setting-up-wsl-with-gpu-support-for-windows-11/), it is highly recommended to install Windows Subsystem for Linux (WSL) to work with Docker in a Linux environment within Windows. Please ensure you install WSL 2 by following the instructions provided by [Microsoft](https://learn.microsoft.com/en-us/windows/wsl/install). Note that the basic version of WSL 2 does not come with GPU support. Please watch the [official tutorial by Microsoft on installing WSL 2 with GPU support](https://www.youtube.com/watch?v=PdxXlZJiuxA). Please note that Docker unfortunately also has issues with GPU support if you are using Windows 10 (need Windows 11).
- Alternatively, you can work purely out of Ubuntu or any other Linux flavor (likely the path of least resistance). In this tutorial, we are working on macOS running a lightweight Linux VM using Alpine Linux.

**Installation Steps:**

1. **Install Docker:**
    - Ensure Docker is installed on your system by following the instructions on the [official Docker website](https://www.docker.com/get-started/). We recommend installing [Docker Desktop](https://www.docker.com/products/docker-desktop/) for ease of use.
2. **Optional (but strongly recommended):**
    - If you want to have GPU support for local testing, install the NVIDIA container toolkit by following the [NVIDIA Docker installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). Note that this does not compromise your building and exporting processes. It only hampers your testing process. You can avoid this by testing with CPU-only mode if possible. Make sure to remove the `--gpus all` flag from test.sh.
3. **Clone this Repository:**
```
git clone https://github.com/kwahid/HNTSMRG_2024.git
```

## **2\. Example Structure Overview**

This repository provides two examples: one for Task 1 (pre-RT segmentation) and another for Task 2 (mid-RT segmentation). Both examples produce a simple segmentation mask output for a given MRI input (or set of MRI inputs in the case of Task 2); no machine learning is used. They are structured similarly and contain the same base files, enabling you to run an example using the provided data for one patient. The main files are:

- **inference.py:** A Python script that contains functions to run the inference for one input patient.
- **requirements.txt:** A text file containing the Python libraries that are required to run inference.py.
- **Dockerfile:** A Dockerfile containing all the system requirements to run the inference.py script.
- **build.sh:** A bash script that will build the Docker container image.
- **test_run.sh:** A bash script that will build and execute the Docker container image using the provided input data for one patient.
- **export.sh:** A bash script that will zip the built Docker container image into a single file for upload to the Grand Challenge website.

## **3\. Embedding an Algorithm into a Docker Container Image**

1. **Modify inference.py:**
    - You can add additional functions, include additional scripts, and import additional Python libraries. You must use the paths defined (inputs, outputs) exactly for your script to work with the Grand Challenge interface.
    - Remember, the Grand Challenge platform will run the Docker container on a patient-by-patient basis; keep this in mind when writing your inference code.
2. **Modify Dockerfile:**
    - Change the base image in the Dockerfile if necessary, e.g., `FROM nvcr.io/nvidia/pytorch:22.12-py3` for Pytorch.
    - Add your model weights and other necessary files. You can place these in the Resources folder or make a new folder (but remember to use the COPY command in the Dockerfile).
    - Your Dockerfile may get fairly complicated if you require many specific installs or dependencies.
3. **Add Required Python Packages:**
    - List all required Python packages in the requirements.txt file to be installed when the container is built.

## **4\. Building your Docker Container Image**

To build the Docker container, run the following command from the root of your project directory:
```
./build.sh
```

Please note that the next steps (testing the container image and zipping the container image) also run a build, so this step is not mandatory.

## **5\. Testing your Docker Container Image**

We have provided sample data in the test/input folder. Task 1 contains an MHA file of a pre-RT image. Task 2 contains MHA files of a mid-RT image, pre-RT image, pre-RT mask, registered pre-RT image, and registered pre-RT mask. The example patient corresponds to patient ID 86 in the training set, which can be found on [Zenodo](https://zenodo.org/records/11199559). This data was converted to MHA format through the GC interface, which is exactly how the input data will be presented to algorithm containers on GC. For reference, the test images are organized as follows:

**Task 1:**
```
test/
└───input
    └───images
        └───pre-rt-t2w-head-neck
            └─── .mha file
└───output
```

**Task 2:**
```
test/
└───input
    └───images
        └───pre-rt-t2w-head-neck
            └─── .mha file
        └───mid-rt-t2w-head-neck
            └─── .mha file
        └───pre-rt-head-neck-segmentation
            └─── .mha file
        └───registered-pre-rt-head-neck (PLEASE SEE NOTE BELOW)
            └─── .mha file 
        └───registered-pre-rt-head-neck-segmentation
            └─── .mha file
└───output
```

Unfortunately, due to GitHub file size upload constraints, we had to remove the MHA file inside the registered-pre-rt-head-neck folder. You can download this file directly from the following [Google Drive location](https://drive.google.com/file/d/1NNE0y6fa_tJaU3AGGMrcj0bzyG305vkd/view?usp=drive_link). Please be sure to place the file inside the correct folder (registered-pre-rt-head-neck).

For the most part, you shouldn’t need to modify the test_run.sh file. **IMPORTANT:** These current examples do not use GPU support. Your scripts likely will, so be sure to enable the --gpus all flag in the docker run command of the test_run.sh file.

To test your container, run:

```
./test.sh
```

This will run the sample image(s) provided in the test folder through your model and save predicted segmentation masks to the output/images/mri-head-neck-segmentation directory. You can then compare these segmentation masks with the ones that you expected to receive from the model. If they match, that's a good sign that your algorithm is working correctly. If not, you should check the inference.py script and make sure that the inference code is correct.

## **6\. Saving your Docker Container Image as a Zip File**

After verifying that your container works correctly, package it for upload to Grand-Challenge.org. To package your Docker container image into a zip file, run:

```
./export.sh
```

This step creates a file with the extension .tar.gz, which you can then upload to Grand Challenge to submit your algorithm. You can alternatively directly run a docker save command (after building the container or running the test.sh script) such as:

```
docker save example-algorithm-task-1-pre-rt-segmentation | gzip -c > example-algorithm-task-1-pre-rt-segmentation.tar.gz
```

## **7\. Submitting an Algorithm (Zipped Docker Container Image) on Grand-Challenge.org**

- Before submitting to the challenge, you should first test your Docker container locally (as outlined above). [This Grand Challenge webpage](https://grand-challenge.org/documentation/building-and-testing-the-container/) might help you with testing.
- In order to submit your Docker container, you first have to create an Algorithm entry at the relevant development/testing phase webpage ([Task 1 development phase here](https://hntsmrg24.grand-challenge.org/evaluation/preliminary-development-phase-task-1-pre-rt-segmentation/submissions/create/), [Task 1 testing phase here](https://hntsmrg24.grand-challenge.org/evaluation/final-test-phase-task-1-pre-rt-segmentation/submissions/create/), [Task 2 development phase here](https://hntsmrg24.grand-challenge.org/evaluation/preliminary-development-phase-task-2-mid-rt-segmentation/submissions/create/), [Task 2 testing phase here](https://hntsmrg24.grand-challenge.org/evaluation/final-test-task-2-mid-rt-segmentation/submissions/create/)).
- After creating an Algorithm entry, you can upload your Docker container to the Algorithm page (or you can also overwrite your container). Overwriting the container is recommended when submitting a new iteration of the same method (e.g., when you fix potential bugs). Depending on the size of the zip file, the upload can take from 15 minutes (a few GBs) to over an hour (10 GBs).
- After uploading your container file, a series of checks will occur to make sure the container can be imported and used without issues. Please note that it can take several minutes until the container becomes active (you can refresh the page to see the status).
- Once your container is imported and active, you can also try out your algorithm on some sample data. You can use one of the training images (NIfTI files from Zenodo, or the provided MHA files from the test/input folder) to test if predictions are as expected. The Grand Challenge website has a results viewer which allows you to visualize your generated segmentations.
- Finally, you can submit your algorithm to the HNTS-MRG Challenge by selecting your algorithm on the relevant phase submission page, whereupon it will be run on the relevant patient cases for that phase.

## **General Remarks**

- Ensure that training is not done as part of the Docker container; only inference should run within the container.
- Verify that the container reads from the /input path and writes to the /output path as specified.
- Submit to the development phase (2 patients) first to debug and verify that your container is working as expected, as you have multiple attempts. Once you are confident, proceed to the final test phase (50 patients), where you will only have one attempt to submit.
