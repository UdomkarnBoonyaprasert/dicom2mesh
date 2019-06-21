#*************assuming that no resample has to be done for ALL nifti files*************

import numpy as np
import nibabel as nib
import fileHandler
import platform

cwd = fileHandler.cwd
slash = fileHandler.slash

numpyPath = cwd + "numpys" + slash
niftiPath = cwd + "imgs" + slash + "nifti" + slash
numpyPath = cwd + "numpys" + slash

fName = ""
tempPath = ""
def getIO():
	fName = fileHandler.getFname(".nii", niftiPath)
	tempPath = niftiPath + fName
	return [tempPath, fName]

def main(mainPath=tempPath, tempFname=fName, option=0):
	#https://github.com/nipy/nibabel/issues/626
	nib.Nifti1Header.quaternion_threshold = -1e-06
	img = nib.load(mainPath)

	a = np.array(img.dataobj)
	if option == 1:
		np.save(numpyPath + "%s.npy" % tempFname[:-4], a)
		return 0
	return a

if __name__ == '__main__':
	lsIO = getIO()
	temp = main(lsIO[0], lsIO[1], 1)
	print(lsIO[1][:-4] + ".npy generated.")