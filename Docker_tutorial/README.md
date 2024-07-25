# **Example Algorithm Docker Container Images for HNTS-MRG 2024 Challenge**

**Authors:** Kareem A. Wahid (<kawahid@mdanderson.org>), Cem Dede (<cdede@mdanderson.org>).

**General Contact Email:** <hntsmrg2024@gmail.com>.

*Note: We would like to thank the authors of the [MIDOG](https://github.com/DeepMicroscopy/MIDOG_reference_docker), [HaN-Seg](https://github.com/gasperpodobnik/HanSeg2023Algorithm?tab=readme-ov-file#export), and [SegRap](https://github.com/HiLab-git/SegRap2023/tree/main?tab=readme-ov-file) challenges for their reference documentation on which this tutorial is based.*

These files serve as templates for preparing algorithm Docker container images for the [HNTS-MRG 2024 Challenge](https://hntsmrg24.grand-challenge.org/). They include scripts and path definitions necessary to run your algorithms on the grand-challenge.org platform. To better understand how algorithms on grand-challenge.org work, you may want to read the blog posts on [how to create an algorithm](https://grand-challenge.org/documentation/create-your-own-algorithm/).

We have also recorded a series of videos that walk you through the first six sections (link will be inserted here later) and submitting an algorithm on Grand-Challenge.org (link will be inserted here later).

## **Table of Contents**

1. [Prerequisites](#1-prerequisites)
2. [Example Files Overview](#2-example-files-overview)
3. [Embedding an Algorithm into a Docker Container Image](#3-embedding-an-algorithm-into-a-docker-container-image)
4. [Building your Docker Container Image](#4-building-your-docker-container-image)
5. [Testing your Docker Container Image](#5-testing-your-docker-container-image)
6. [Saving your Docker Container Image as a Zip File](#6-saving-your-docker-container-image-as-a-zip-file)
7. [Submitting an Algorithm (Zipped Docker Container Image) on Grand-Challenge.org](#7-submitting-an-algorithm-zipped-docker-container-image-on-grand-challengeorg)
8. [General Remarks](#8-general-remarks)


## **1\. Prerequisites**

**Recommendations for Windows Users:**

- As per the [Grand Challenge documentation](https://grand-challenge.org/documentation/setting-up-wsl-with-gpu-support-for-windows-11/), it is highly recommended to install Windows Subsystem for Linux (WSL) to work with Docker in a Linux environment within Windows. Please ensure you install WSL 2 by following the instructions provided by [Microsoft](https://learn.microsoft.com/en-us/windows/wsl/install).
- *Note that the basic version of WSL 2 does not come with GPU support. Please watch the [official tutorial by Microsoft on installing WSL 2 with GPU support](https://www.youtube.com/watch?v=PdxXlZJiuxA).* 
- Alternatively, you can work purely out of Ubuntu or any other Linux flavor (likely the path of least resistance, Windows almost always has some issues pop up). In this tutorial, we are working on macOS running a lightweight Linux VM using Alpine Linux.

**Installation Steps:**

- **Install Docker:**
    - Ensure Docker is installed on your system by following the instructions on the [official Docker website](https://www.docker.com/get-started/).
    - We recommend installing [Docker Desktop](https://www.docker.com/products/docker-desktop/) for ease of use.
- **Optional (but strongly recommended):**
    - If you want to have GPU support for local testing, install the NVIDIA container toolkit by following the [NVIDIA Docker installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). *Note that this does not compromise your building and exporting processes. It only hampers your testing process.* You can avoid this by testing with CPU-only mode if possible. Make sure to remove the `--gpus all` flag from `test_run.sh`.
- **Clone this Repository:**
```
git clone https://github.com/kwahid/HNTSMRG_2024.git
```

## **2\. Example Files Overview**

This repository provides two examples: an example for Task 1 (pre-RT segmentation) and another example for Task 2 (mid-RT segmentation). Both examples produce a simple segmentation mask output for a given MRI input (or set of MRI inputs in the case of Task 2); no deep learning is used. They are structured similarly and contain the same base files, enabling you to run an example using the provided data for one patient. The main files are:

- **`inference.py`:** A Python script that contains functions to run the inference for one input patient.
- **`requirements.txt`:** A text file containing the Python libraries that are required to run `inference.py`.
- **`Dockerfile`:** A Dockerfile containing all the system requirements to run the `inference.py` script.
- **`build.sh`:** A bash script that will build the Docker container image.
- **`test_run.sh`:** A bash script that will build and execute the Docker container image using the provided input data for one patient contained in `test/input`.
- **`export.sh`:** A bash script that will zip the built Docker container image into a single file for upload to the Grand Challenge website.

For Windows users who do not want to use WSL, we have also provided analagous .bat files (`build.bat`, `test_run.bat`. `export.bat`). But again, we suggest using WSL instead. 

## **3\. Embedding an Algorithm into a Docker Container Image**

1. **Modify `inference.py`:**
    - You can add additional functions, include additional scripts, and import additional Python libraries.
        - You must use the paths defined (inputs, outputs) exactly for your script to work with the Grand Challenge interface.
        - The *size, spacing, origin, and direction* of the generated prediction masks should be the same as the corresponding MRI for the given task (i.e., pre-RT image for Task 1, mid-RT image for Task 2). You can use `output_sitk_img.CopyInformation(input_sitk_img)` to copy the origin, spacing and direction values from the input image to the output image to ensure they correspond.
    - *Note: The Grand Challenge platform will run the Docker container for each patient separately. There is a hard-limit 15-minute run-time. This means you should be cognizant of factors like implementing a large number of ensembles or time-sensitive registration processes in your algorithm.*
2. **Modify `Dockerfile`:**
    - Change the base image in the Dockerfile if necessary, e.g., `FROM nvcr.io/nvidia/pytorch:22.12-py3` for Pytorch.
    - Add your model weights and other necessary files. You can place these in the `/resources` folder or make a new folder (but remember to use the `COPY` command in the Dockerfile).
    - *Note: Your Dockerfile may get fairly complicated if you require many specific installs or dependencies. This often is the main factor for large final Docker container image sizes. Your final zipped Docker container image must be < 10 GB to be uploaded to the Grand Challenge.*
3. **Add Required Python Packages:**
    - List all required Python packages in the `requirements.txt` file to be installed when the container is built.

All Docker containers submitted to the challenge will be run in an offline setting (i.e. they will not have access to the internet, and cannot download/upload any resources). All necessary resources (e.g. pre-trained weights) must be encapsulated in the submitted containers a priori.

## **4\. Building your Docker Container Image**

To build the Docker container image, run the following command from the root of your project directory:
```
./build.sh
```

*Note: The next steps (testing the container image and zipping the container image) also run a build, so this step is not mandatory.*

## **5\. Testing your Docker Container Image**

We have provided sample data in the `test/input` folder. Task 1 contains an MHA file of a pre-RT image. Task 2 contains MHA files of a mid-RT image, pre-RT image, pre-RT mask, registered pre-RT image, and registered pre-RT mask. The example patient corresponds to patient ID 86 in the training set, which can be found on [Zenodo](https://zenodo.org/records/11199559). This data was converted to MHA format through the Grand Challenge interface, which is exactly how the input data will be presented to algorithm containers on Grand Challenge. For reference, the sample images are organized as follows:

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

Unfortunately, due to GitHub file size upload constraints, we had to remove the MHA file inside the `registered-pre-rt-head-neck folder`. You can download this file directly from the following [Google Drive location](https://drive.google.com/file/d/1NNE0y6fa_tJaU3AGGMrcj0bzyG305vkd/view?usp=drive_link). Please be sure to place the file inside the correct folder (`registered-pre-rt-head-neck`).

For the most part, you shouldn’t need to modify the `test_run.sh` file. 
**IMPORTANT:** These current examples do not use GPU support. Your scripts likely will, so be sure to enable the `--gpus all` flag in the docker run command of the `test_run.sh` file.

To test your container, run:

```
./test_run.sh
```

This will run your model on the sample data and save predicted segmentation masks to the output/images/mri-head-neck-segmentation directory. The output will look like the following:

```
test/
└───output
    └───images
        └─── mri-head-neck-segmentation
            └─── output.mha file
```

You can then compare this segmentation masks with the one that you expected to receive from the model. If they match, that's a good sign that your algorithm is working correctly. If not, you should check the inference.py script and make sure that the inference code is correct.

## **6\. Saving your Docker Container Image as a Zip File**

After verifying that your container works correctly, package it for upload to Grand-Challenge.org. To package your Docker container image into a zip file, run:

```
./export.sh
```

This step creates a file with the extension .tar.gz, which you can then upload to Grand Challenge to submit your algorithm (*keep in mind the 10GB zip file size limit*). You can alternatively directly run a docker save command (after building the container or running the `test_run.sh` script) such as:

```
docker save example-algorithm-task-1-pre-rt-segmentation | gzip -c > example-algorithm-task-1-pre-rt-segmentation.tar.gz
```

## **7\. Submitting an Algorithm (Zipped Docker Container Image) on Grand-Challenge.org**

Before submitting to the challenge, you should first test your Docker container locally (as outlined above). [This Grand Challenge webpage](https://grand-challenge.org/documentation/building-and-testing-the-container/) might further help you with testing. The following are general steps for submitting the container on the Grand Challenge website. More detailed instructions (with screenshots) can be found on the [Submission Instructions page for HNTS-MRG 2024](https://hntsmrg24.grand-challenge.org/submission-instructions/).

**General Steps to Submit Your Docker Container**
1. **Create an Algorithm Entry:**
    - Navigate to the relevant development/testing phase webpage:
        - [Task 1 development phase](https://hntsmrg24.grand-challenge.org/evaluation/preliminary-development-phase-task-1-pre-rt-segmentation/submissions/create/)
        - [Task 1 testing phase](https://hntsmrg24.grand-challenge.org/evaluation/final-test-phase-task-1-pre-rt-segmentation/submissions/create/)
        - [Task 2 development phase](https://hntsmrg24.grand-challenge.org/evaluation/preliminary-development-phase-task-2-mid-rt-segmentation/submissions/create/)
        - [Task 2 testing phase](https://hntsmrg24.grand-challenge.org/evaluation/final-test-task-2-mid-rt-segmentation/submissions/create/)
    - Create a new Algorithm entry for your submission.
2. **Upload Your Docker Container:**
    - Once the Algorithm entry is created, upload your Docker container to the Algorithm page. You can also overwrite an existing container if you are submitting a new iteration of the same method (e.g., fixing bugs).
    - *Note: Depending on the size of the zip file, the upload process can take from 15 minutes (a few GBs) to over an hour (10 GBs).*
3. **Validation and Activation:**
    - After uploading, the system will perform a series of checks to ensure the container can be imported and used without issues.
    - *Note: This process can take several minutes. You can refresh the page to check the status.*
4. **Try-out Algorithm and Visualize Results:**  
    - Once your container is imported and active, you can also ["try out" your algorithm](https://grand-challenge.org/documentation/try-out-your-algorithm/) on some sample data. You can use one of the training images (NIfTI files from Zenodo, or the provided MHA files from the `test/input` folder) to test if predictions are as expected.
    - The Grand Challenge website has an online results viewer which allows you to visualize your generated segmentations.
5. **Submit to the Challenge:**  
    - Select your algorithm on the relevant phase submission page. Your algorithm will then be run on the relevant patient cases for that phase.

## **8\. General Remarks**

- **Inference Only:** Ensure that training is not part of the Docker container; only inference should run within the container.
- **Path Specifications:** Verify that the container reads from the `/input` path and writes to the `/output` path as specified.
- **Development Phase Submission:** Submit to the development phase (2 patients) first to debug and verify that your container is working as expected, as you have multiple attempts available.
- **Final Test Phase Submission:** Once you are confident in your algorithm's performance, proceed to the final test phase (50 patients), where you will have only one attempt to submit.
- **GitHub Integration:** As an alternative to building your container image locally, zipping, and uploading, you can instead link a GitHub repository to your algorithm on Grand Challenge (a new container image will be built automatically each time the repository is tagged). While we do not provide detailed instructions here, you can find comprehensive guidance on the [Grand Challenge website](https://grand-challenge.org/documentation/linking-a-github-repository-to-your-algorithm/). 
- **Reach out to us!:** If this is your first time working with Docker/Grand-Challenge or anything is confusing, please don’t hesitate to reach out to us with questions (<hntsmrg2024@gmail.com>). We are here to help and happy to jump on a Zoom call to debug. The last thing we want is for this to be a bottleneck to you submitting your algorithm for the challenge. 

