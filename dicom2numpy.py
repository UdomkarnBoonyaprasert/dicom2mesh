import numpy as np
import pydicom as dicom
import pydicom.pixel_data_handlers.gdcm_handler
import os
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
import fileHandler

#-----------Unix uses "/", whereas Windows uses "\"-----------
slash = "/"
runningPlatform = platform.system()
if runningPlatform == "Windows":
	slash = "\\"
#-------------------------------------------------------------

cwd = os.getcwd() + slash

fName = fileHandler.getFname()
fillPath = fileHandler.dicomPath + str(fName)

def load_scan(path):
	slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
	slices.sort(key = lambda x: int(x.InstanceNumber))
	try:
		slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
	except:
		slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
		
	for s in slices:
		s.SliceThickness = slice_thickness
		
	return slices




def resample(image, scan, new_spacing=[1,1,1]):
	patient = load_scan(data_path)
	fileoption_resamp = fileoption[:-6]+("%d.npy"%id)
	imgs_to_process = np.load(output_path+fileoption_resamp)#'fullimages_{}.npy'+fileoption.format(id)
	# Determine current pixel spacing
	try:
		spacing = map(float, ([scan[0].SliceThickness] + [patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]]))
		spacing = np.array(list(spacing))
	except:
		print(len(patient[0].PixelSpacing))
		print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))
		print("something went sooooooooooooooooooooooooooooo wrong")
		exit()

	resize_factor = spacing / new_spacing
	new_real_shape = image.shape * resize_factor
	new_shape = np.round(new_real_shape)
	real_resize_factor = new_shape / image.shape
	new_spacing = spacing / real_resize_factor
	
	image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
	
	return image, new_spacing

print ("Shape before resampling\t", imgs_to_process.shape)
imgs_after_resamp, spacing = resample(imgs_to_process, patient, [1,1,1])
print ("Shape after resampling\t", imgs_after_resamp.shape)


np.save(numpyPath + "%s.npy" % fName[:-4], imgs_after_resamp)


