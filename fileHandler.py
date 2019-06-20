import os
import platform

#-----------Unix uses "/", whereas Windows uses "\"-----------
slash = "/"
runningPlatform = platform.system()
if runningPlatform == "Windows":
	slash = "\\"
#-------------------------------------------------------------

cwd = os.getcwd() + slash

dicomPath = cwd + "imgs" + slash + "dicom" + slash
niftiPath = cwd + "imgs" + slash + "nifti" + slash
outputPath = cwd + "outputs" + slash
numpyPath = cwd + "numpys" + slash


def getFname(reqFileType=".npy", fPath=os.getcwd() + slash):
	if reqFileType == "dir":
		fileChoice = input("please enter the foldername with imgs, or enter 'lsdir' to select an itemfrom a list:  ")
	else:
		fileChoice = input("Please enter '{0}' file name (with '{1}' extension), or enter 'lsdir' to select an item from a list:  ".format(reqFileType, reqFileType))
	if fileChoice == "lsdir":
		lsdirNumpy = os.listdir(fPath)
		if len(lsdirNumpy) == 0:
			print("No munpy file found, exiting...")
			exit()
		counter = 0
		for direc in lsdirNumpy:
			print(str(counter) + ".)\t" + direc)
			counter = counter + 1
		tempInt = input("Please enter choice(int):  ")
		fileChoice = str(lsdirNumpy[int(tempInt)])
	if reqFileType != "dir" and fileChoice[len(fileChoice)-(len(reqFileType)):] != reqFileType:
		print("Not a valid file choice, exiting...")
		exit()
	return fileChoice

