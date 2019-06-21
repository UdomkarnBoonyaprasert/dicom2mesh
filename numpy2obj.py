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
import time
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
import fileHandler

nib.Nifti1Header.quaternion_threshold = -1e-06

slash = fileHandler.slash
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

def getIO():
	fName = fileHandler.getFname(".npy", numpyPath)
	tempPath = fileHandler.dicomPath + str(fName) + slash
	thresholdinput = input("Please enter HU threshold(int):  ")
	return [tempPath, fName, thresholdinput]
#fileChoice = fileHandler.getFname(".npy", numpyPath)


#thresholdinput = input("Please enter HU threshold(int):  ")
#v, f, n = make_mesh(imgs_after_resamp, int(thresholdinput), 1)#350
#plt_3d(v, f)

start = time.time()


def makeObj(fPath, thisThreshold, objOutput):
	if str(type(fPath)) == "<class 'numpy.ndarray'>":
		tempnumpy = fPath
	else:
		try:
			tempnumpy = np.load(numpyPath + fPath)
		except:
			print("Something went wrong with the numpy loading process, exiting...")
			exit()

	v, f, n = make_mesh(tempnumpy, int(thisThreshold), 1)#350


	f=f+1#not sure why we need this. the mesh looks 'weird' without it      solution ref >>>>>>   https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python      18/06/19


	#objOutput = input("Please enter name for 'obj' file(without .obj extension):  ")
	newObj = open(outputPath + 'OBJs/%s.obj' % objOutput, 'w')
	for item in v:
		newObj.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))

	for item in n:
		newObj.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))

	for item in f:
		newObj.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
	newObj.close()


def main(mainFchoice, mainThreshold):
	makeObj(mainFchoice, mainThreshold)

def main(mainFchoice, mainThreshold, outputName):
	makeObj(mainFchoice, mainThreshold, outputName)

if __name__ == '__main__':
	lsIO = getIO()
	tempInput = input("Please enter name for 'obj' file(without .obj extension), or leave blank for the same name as .npy:  ")
	if str(tempInput) == "":
		tempInput = lsIO[1]
	main(lsIO[1], lsIO[2], tempInput)

	timeTaken = time.time() - start
	print ("Task finsished. Time taken to generate mesh:  " + str(timeTaken) + " seconds")



