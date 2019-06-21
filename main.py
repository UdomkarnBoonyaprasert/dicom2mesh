#OBJ2GLTF >>>>> https://github.com/AnalyticalGraphicsInc/obj2gltf, https://github.com/mrdoob/three.js
import nifti2numpy
import dicom2numpy
import numpy2obj
import fileHandler
import sys

slash = fileHandler.slash
argCount = len(sys.argv)

if argCount < 4:
	print("Invalid number of argument.")

option = sys.argv[1]
fname = str(sys.argv[2])
threshold = sys.argv[3]
foutput = str(sys.argv[4])
#npysaveoption = sys.argv[5]#not here yet (option to save npy)

if option == 1 or str(option) == "d":#dicom
	tempNpy = dicom2numpy.main(fileHandler.dicomPath + slash + fname, fname)#not done
	if argCount == 5:
		numpy2obj.main(tempNpy, threshold, foutput)
	else:
		numpy2obj.main(tempNpy, threshold)

elif option == 2 or str(option) == "n":#nifti
	tempNpy = nifti2numpy.main(fileHandler.niftiPath + slash + fname, fname)#not done
	if argCount == 5:
		numpy2obj.main(tempNpy, threshold, foutput)
	else:
		numpy2obj.main(tempNpy, threshold)

elif option == 3 or str(option) == "num":#numpy
	if argCount == 5:
		numpy2obj.main(tempNpy, threshold, foutput)
	else:
		numpy2obj.main(tempNpy, threshold)
	print ("Numpy to obj conversion, done")