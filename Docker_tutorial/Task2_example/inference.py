"""
The following is a simple example algorithm for Task 2 (mid-RT segmentation) of the HNTS-MRG 2024 challenge.

It is meant to run within a container.

To run it locally, you can call the following bash script:

  ./test_run.sh

This will start the inference and reads from ./test/input and outputs to ./test/output

To export the container and prep it for upload to Grand-Challenge.org you can call:

  docker save example-algorithm-task-2-mid-rt-segmentation | gzip -c > example-algorithm-task-2-mid-rt-segmentation.tar.gz

Any container that shows the same behavior will do, this is purely an example of how one COULD do it.

Happy programming!
"""

from pathlib import Path
from glob import glob
import SimpleITK as sitk
import numpy as np

INPUT_PATH = Path("/input") # these are the paths that Docker will use
OUTPUT_PATH = Path("/output")
RESOURCE_PATH = Path("resources")

def run():
    """
    Main function to read input, process the data, and write output.
    """

    ### 1. Read the input(s) from the correct path(s). 
    # Currently reads input as a SimpleITK image. You should only need to read in the inputs that your algorithm uses. 
    mid_rt_t2w_head_neck = load_image_file(
        location=INPUT_PATH / "images/mid-rt-t2w-head-neck", # Make sure to read from this path; this is exactly how the Grand Challenge will give the input to your container.
    )
    pre_rt_t2w_head_neck = load_image_file(
        location=INPUT_PATH / "images/pre-rt-t2w-head-neck", # Make sure to read from this path; this is exactly how the Grand Challenge will give the input to your container.
    )
    pre_rt_head_neck_segmentation = load_image_file(
        location=INPUT_PATH / "images/pre-rt-head-neck-segmentation", # Make sure to read from this path; this is exactly how the Grand Challenge will give the input to your container.
    )
    registered_pre_rt_head_neck = load_image_file(
        location=INPUT_PATH / "images/registered-pre-rt-head-neck", # Make sure to read from this path; this is exactly how the Grand Challenge will give the input to your container.
    )
    registered_pre_rt_head_neck_segmentation = load_image_file(
        location=INPUT_PATH / "images/registered-pre-rt-head-neck-segmentation", # Make sure to read from this path; this is exactly how the Grand Challenge will give the input to your container.
    )
    
    ### 2. Process the inputs any way you'd like. 
    # This is where you should place your relevant inference code.
    _show_torch_cuda_info()

    with open(RESOURCE_PATH / "some_resource.txt", "r") as f:
        print(f.read())

    # Generate a segmentation cube in the middle of the image
    segmentation = generate_segmentation(registered_pre_rt_head_neck_segmentation) # This just a toy example. Make sure to replace this with your inference code.
    
    ### 3. Save your output to the correct path. 
    # Currently takes generated mask (in SimpleITK image format) and writes to MHA file. 
    write_mask_file(
        location=OUTPUT_PATH / "images/mri-head-neck-segmentation", # Make sure to write to this path; this is exactly how the Grand Challenge will expect the output from your container.
        segmentation_image=segmentation,
    )
    
    return 0


def load_image_file(*, location):
    # Use SimpleITK to read a file
    input_files = glob(str(location / "*.mha")) # Grand Challenge uses MHA files 
    result = sitk.ReadImage(input_files[0])

    # Return the sitk image
    return result


def generate_segmentation(segmentation_input):
    """
    Simple example algorithm that uses avaliable pre-RT segmentation mask as a starting point. Erodes label 1 in a segmentation mask and combines it with the original label 2. In other words, the GTVp shrinks and the GTVn stays the same.

    This function takes a pre-RT head and neck segmentation mask as input, erodes label 1 on each 2D axial slice,
    and combines it with the original label 2. The erosion radius is calculated as 20% of the mask size in each slice.
    """
    # Convert image to numpy array for manipulation
    segmentation_array = sitk.GetArrayFromImage(segmentation_input)
    
    # Separate labels 1 and 2
    label1 = segmentation_array == 1
    label2 = segmentation_array == 2

    # Erode label 1 on each 2D axial slice
    eroded_label1 = np.zeros_like(label1)
    for i in range(label1.shape[0]):
        slice_label1 = label1[i].astype(np.uint8)
        if np.any(slice_label1):  # Check if the slice has label 1
            slice_image = sitk.GetImageFromArray(slice_label1)
            # Calculate the erosion radius as 20% of the mask size in this slice, higher % equals more aggresive erosion
            label1_size = np.sum(slice_label1)
            erosion_radius = int(np.sqrt(label1_size) * 0.2)
            erosion_radius = [erosion_radius] * slice_image.GetDimension()
            eroded_slice_label1 = sitk.GetArrayFromImage(sitk.BinaryErode(slice_image, erosion_radius))
            eroded_label1[i] = eroded_slice_label1
    
    # Combine eroded label 1 and original label 2
    eroded_segmentation = np.where(eroded_label1, 1, np.where(label2, 2, 0))
    
    # Convert back to SimpleITK image
    segmentation_image = sitk.GetImageFromArray(eroded_segmentation.astype(np.uint8))
    segmentation_image.CopyInformation(segmentation_input)
    
    return segmentation_image


def write_mask_file(*, location, segmentation_image):
    location.mkdir(parents=True, exist_ok=True)

    # Cast the segmentation image to 8-bit unsigned int
    segmentation_image = sitk.Cast(segmentation_image, sitk.sitkUInt8)
    
    # Convert the numpy array back to a SimpleITK image
    suffix = ".mha"
    sitk.WriteImage(segmentation_image, location / f"output{suffix}", useCompression=True)


def _show_torch_cuda_info():
    import torch

    print("=+=" * 10)
    print("Collecting Torch CUDA information")
    print(f"Torch CUDA is available: {(available := torch.cuda.is_available())}")
    if available:
        print(f"\tnumber of devices: {torch.cuda.device_count()}")
        print(f"\tcurrent device: { (current_device := torch.cuda.current_device())}")
        print(f"\tproperties: {torch.cuda.get_device_properties(current_device)}")
    print("=+=" * 10)


if __name__ == "__main__":
    raise SystemExit(run())