"""
The following is a simple example algorithm for Task 1 (pre-RT segmentation) of the HNTS-MRG 2024 challenge.

It is meant to run within a container.

To run it locally, you can call the following bash script:

  ./test_run.sh

This will start the inference and reads from ./test/input and outputs to ./test/output

To export the container and prep it for upload to Grand-Challenge.org you can call:

  docker save example-algorithm-task-1-pre-rt-segmentation | gzip -c > example-algorithm-task-1-pre-rt-segmentation.tar.gz

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
    
    ### 1. Read the input from the correct path. 
    # Currently reads input as a SimpleITK image. 
    pre_rt_t2w_headneck = load_image_file(
        location = INPUT_PATH / "images/pre-rt-t2w-head-neck", # Make sure to read from this path; this is exactly how the Grand Challenge will give the input to your container.
    )
    
    ### 2. Process the inputs any way you'd like. 
    # This is where you should place your relevant inference code.
    _show_torch_cuda_info()

    with open(RESOURCE_PATH / "some_resource.txt", "r") as f:
        print(f.read())

    segmentation = generate_segmentation(pre_rt_t2w_headneck) # This just a toy example. Make sure to replace this with your inference code.
    
    ### 3. Save your output to the correct path. 
    # Currently takes generated mask (in SimpleITK image format) and writes to MHA file. 
    write_mask_file(
        location = OUTPUT_PATH / "images/mri-head-neck-segmentation", # Make sure to write to this path; this is exactly how the Grand Challenge will expect the output from your container.
        segmentation_image = segmentation,
    )
    
    return 0


def load_image_file(*, location):
    # Use SimpleITK to read a file
    input_files = glob(str(location / "*.mha")) # Grand Challenge uses MHA files 
    result = sitk.ReadImage(input_files[0])

    # Return the sitk image
    return result


def generate_segmentation(image):
    """
    Simple example algorithm. Generates a segmentation with a central cube and a smaller adjacent cube. Outputs the mask in SimpleITK image format. 

    This function takes a MRI image as input and creates a segmentation mask.
    The segmentation contains two labeled regions:
      1. A central cube of 50 mm side length centered in the image (corresponds to GTVp).
      2. A smaller cube of 30 mm side length adjacent to the central cube (corresponds to GTVn).
    """
    
    # Get image properties
    spacing = image.GetSpacing()
    size = image.GetSize()
    
    # Convert image to numpy array for manipulation
    image_array = sitk.GetArrayFromImage(image)
    segmentation = np.zeros_like(image_array)
    
    # Calculate the center of the image
    center = np.array(size) // 2
    
    # Calculate the size of the central cube in voxels (50 mm all around)
    central_cube_size_voxels = (50.0 / np.array(spacing)).astype(int)
    
    # Define the region for the central cube
    start_cube = center - central_cube_size_voxels // 2
    end_cube = start_cube + central_cube_size_voxels
    
    # Ensure the cube is within bounds
    start_cube = np.maximum(start_cube, 0)
    end_cube = np.minimum(end_cube, np.array(size))
    
    # Create the central cube in the segmentation array
    segmentation[start_cube[2]:end_cube[2], start_cube[1]:end_cube[1], start_cube[0]:end_cube[0]] = 1
    
    # Calculate the size of the smaller cube (30 mm all around)
    small_cube_size_voxels = (30.0 / np.array(spacing)).astype(int)
    
    # Define the region for the smaller cube adjacent to the main cube
    start_left_cube = start_cube.copy()
    start_left_cube[0] = start_cube[0] - small_cube_size_voxels[0] - 1
    end_left_cube = start_left_cube + small_cube_size_voxels
    start_left_cube = np.maximum(start_left_cube, 0)
    end_left_cube = np.minimum(end_left_cube, np.array(size))
    
    # Create the smaller cube in the segmentation array with label 2
    segmentation[start_left_cube[2]:end_left_cube[2], start_left_cube[1]:end_left_cube[1], start_left_cube[0]:end_left_cube[0]] = 2
    
    # Convert the numpy array back to a SimpleITK image
    segmentation_image = sitk.GetImageFromArray(segmentation)
    segmentation_image.CopyInformation(image)

    return segmentation_image


def write_mask_file(*, location, segmentation_image):
    location.mkdir(parents=True, exist_ok=True)

    # Cast the segmentation image to 8-bit unsigned int
    segmentation_image = sitk.Cast(segmentation_image, sitk.sitkUInt8)
    
    # Write to a MHA file
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