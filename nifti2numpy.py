#*************assuming that no resample has to be done for ALL nifti files*************

import numpy as np
import nibabel as nib
import fileHandler
import platform

#-----------Unix uses "/", whereas Windows uses "\"-----------
slash = "/"
runningPlatform = platform.system()
if runningPlatform == "Windows":
	slash = "\\"
#-------------------------------------------------------------

cwd = fileHandler.cwd

numpyPath = cwd + "numpys" + slash
niftiPath = cwd + "imgs" + slash + "nifti" + slash
numpyPath = cwd + "numpys" + slash

fName = fileHandler.getFname(".nii", niftiPath)
tempPath = niftiPath + fName

def main(mainPath=tempPath, tempFname=fName):
	#https://github.com/nipy/nibabel/issues/626
	nib.Nifti1Header.quaternion_threshold = -1e-06
	img = nib.load(tempPath)

	a = np.array(img.dataobj)
	np.save(numpyPath + "%s.npy" % fName[:-4], a)

main()