import numpy as np
import pydicom as dicom
import pydicom.pixel_data_handlers.gdcm_handler
import os
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
import fileHandler
import time

slash = fileHandler.slash
cwd = os.getcwd() + slash

def getIO():
	fName = fileHandler.getFname("dir", fileHandler.dicomPath)
	tempPath = fileHandler.dicomPath + str(fName) + slash
	return [tempPath, fName]

def load_scan(scanPath=fileHandler.dicomPath + "samples" + slash):
	slices = [dicom.read_file(scanPath + slash + s) for s in os.listdir(scanPath)]
	slices.sort(key = lambda x: int(x.InstanceNumber))
	try:
		slice_thickness = np.abs(slices[0].ImagePositionscan[2] - slices[1].ImagePositionscan[2])
	except:
		slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
		
	for s in slices:
		s.SliceThickness = slice_thickness
		
	return slices


def get_pixels_hu(scans):
	image = np.stack([s.pixel_array for s in scans])
	# Convert to int16 (from sometimes int16), 
	# should be possible as values should always be low enough (<32k)
	image = image.astype(np.int16)

	# Set outside-of-scan pixels to 1
	# The intercept is usually -1024, so air is approximately 0
	image[image == -2000] = 0
	
	# Convert to Hounsfield units (HU)
	intercept = scans[0].RescaleIntercept
	slope = scans[0].RescaleSlope
	
	if slope != 1:
		image = slope * image.astype(np.float64)
		image = image.astype(np.int16)
		
	image += np.int16(intercept)
	
	return np.array(image, dtype=np.int16)




def resample(dataPath=fileHandler.dicomPath + slash + "samples", new_spacing=[1,1,1]):#was:   def resample(image, scan, new_spacing=[1,1,1], dataPath=fullPath):
	scan = load_scan(dataPath)
	image = get_pixels_hu(scan)
	print ("Shape before resampling\t", image.shape)
	#TODO: add timer
	start = time.clock()
	# Determine current pixel spacing
	try:
		spacing = map(float, ([scan[0].SliceThickness] + [scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]]))
		spacing = np.array(list(spacing))
	except:
		print(len(scan[0].PixelSpacing))
		print ("Pixel Spacing (row, col): (%f, %f) " % (scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]))
		print("something went sooooooooooooooooooooooooooooo wrong")
		exit()

	resize_factor = spacing / new_spacing
	new_real_shape = image.shape * resize_factor
	new_shape = np.round(new_real_shape)
	real_resize_factor = new_shape / image.shape
	new_spacing = spacing / real_resize_factor
	
	image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
	print ("Resample done in:  " + str(time.clock()-start))
	print ("Shape after resampling\t", image.shape)
	
	return image, new_spacing

def main(inputPath=fileHandler.dicomPath + slash + "samples", mainFname="samples", option=0):
	imgs_after_resamp, spacing = resample(inputPath)
	if option == 1:
		np.save(fileHandler.numpyPath + "%s.npy" % mainFname, imgs_after_resamp)
		return 0
	return imgs_after_resamp

if __name__ == '__main__':
	lsIO = getIO()
	temp = main(lsIO[0], lsIO[1], 1)
	print(lsIO[1] + ".npy generated.")


