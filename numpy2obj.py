#%reload_ext signature
#%matplotlib inline
#https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/      14/06/19
#https://wiki.idoimaging.com/index.php?title=Sample_Data   seems like the have some dicoms and a bit of niftis we can playwith    17/06/19
#https://www.researchgate.net/post/What_is_the_easiest_way_to_batch_resize_DICOM_files to down sample dicoms, incase if they're too large  17/06/19
#https://stackoverflow.com/questions/55560243/resize-a-dicom-image-in-python      this one is for python. the one above is for mathlab, i didn't see
#https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python   export mesh to obj   17/06/19

import numpy as np
import nibabel as nib
import pydicom as dicom
import pydicom.pixel_data_handlers.gdcm_handler
import os
import platform
import time
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans

nib.Nifti1Header.quaternion_threshold = -1e-06

#-----------Unix uses "/", whereas Windows uses "\"-----------
slash = "/"
runningPlatform = platform.system()
if runningPlatform == "Windows":
	slash = "\\"
#-------------------------------------------------------------

cwd = os.getcwd() + slash

imgPath = cwd + "imgs" + slash
outputPath = cwd + "outputs" + slash
numpyPath = cwd + "numpys" + slash


def make_mesh(image, threshold=300, step_size=1):
	print ("Transposing surface...")
	p = image.transpose(2,1,0)
	
	print ("Calculating surface...")
	#https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.marching_cubes_lewiner
	verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold, step_size=step_size, allow_degenerate=True) 
	return verts, faces, norm

lsdirNumpy = os.listdir(numpyPath)

fileChoice = input("Please enter numpy file name (with .npy extension), or enter 'lsdir' to select from a list:  ")
if fileChoice == "lsdir":
	lsdirNumpy = os.listdir(numpyPath)
	if len(lsdirNumpy) == 0:
		print("No munpy file found, exiting...")
		exit()
	counter = 0
	for direc in lsdirNumpy:
		print(str(counter) + ".)\t" + direc)
		counter = counter + 1
	tempInt = input("Please enter choice(int):  ")
	fileChoice = str(lsdirNumpy[int(tempInt)])
if fileChoice[len(fileChoice)-4:] != ".npy":
	print("Not a valid file choice(.npy), exiting...")
	exit()

try:
	tempnif = np.load(numpyPath + fileChoice)
except:
	print("Something went wrong with the numpy loading process, exiting...")
	exit()
thresholdinput = input("Please enter HU threshold(int):  ")
#v, f, n = make_mesh(imgs_after_resamp, int(thresholdinput), 1)#350
#plt_3d(v, f)

start = time.time()

v, f, n = make_mesh(tempnif, int(thresholdinput), 1)#350


f=f+1#not sure why we need this. the mesh looks 'weird' without it      solution ref >>>>>>   https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python      18/06/19


objOutput = input("Please enter name for 'obj' file(without .obj extension):  ")
newObj = open(outputPath + 'OBJs/%s.obj' % objOutput, 'w')
for item in v:
	newObj.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))

for item in n:
	newObj.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))

for item in f:
	newObj.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
newObj.close()

timeTaken = time.time() - start

print ("Task finsished. Time taken to generate mesh:  " + str(timeTaken) + " seconds")


