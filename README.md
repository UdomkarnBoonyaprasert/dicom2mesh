# dicom2mesh
A simple Python script which utilises marching cubes algorithm(skimage library) to generate 3D mesh from Dicom/Nifti image stack, which then can be output to .obj file(can be previewed using 3D viewer from microsoft store).

## Requirements:
Python 3.7 or above

## Dependencies:
- Numpy https://www.numpy.org/
- Scipy https://www.scipy.org/
- Pydicom https://pydicom.github.io/
- Skit-image https://scikit-image.org/
- Sklearn https://scikit-learn.org/stable/
- NiBabel https://nipy.org/nibabel/
- Matplotlib https://pypi.org/project/matplotlib/

## Usage:
- The code works by first converting Dicom or Nifti images to a Numpy array, then generate a .obj mesh from it.
- dicom2numpy.py, nifti2numpy.py and numpy2obj.py can be run independently:
> python3 dicom2numpy.py

- For a one way Dicom/Nifti to obj mesh, main.py can be used.
    - An example usage of main.py: 
> python3 main.py "d" "samples" 300 "abdomen_mesh"

   - "d", first argument being the option used for conversion. {"d":dicom to obj, "n":nifti to obj, "num"numpy to obj}
   - "samples", input directory of the Dicom files. Please note that the script can only take input from a fixed directory according           to its conversion option at the moment. {"d": imgs/dicom/(sub dir name), "n": imgs/nifti/(.nii file name), "num": numpy/(.npy             filename)}
   - 300, third argument being the Housfield used for the thresholding in marching cube algorithm. In this example, 300 is used for             bones. For the sample Nifti file please use 30 or above as it has already been segmented.
   - "abdomen_mesh", the fourth argument. Once the mesh has successfully generated, it will be saved in output/OBJs with the given             name.

## OBJ conversion to GLTF/GLB
https://github.com/AnalyticalGraphicsInc/obj2gltf
Make sure to have the latest version of Node.js 

### Refs:
- https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/      14/06/19
- https://wiki.idoimaging.com/index.php?title=Sample_Data   seems like the have some dicoms and a bit of niftis we can playwith    17/06/19
- https://www.researchgate.net/post/What_is_the_easiest_way_to_batch_resize_DICOM_files to down sample dicoms, incase if they're too large  17/06/19
- https://stackoverflow.com/questions/55560243/resize-a-dicom-image-in-python      this one is for python. the one above is for mathlab, i didn't see
- https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python   export mesh to obj   17/06/19
