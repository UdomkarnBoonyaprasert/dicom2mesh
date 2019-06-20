#%reload_ext signature
#%matplotlib inline
#https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/      14/06/19
#https://wiki.idoimaging.com/index.php?title=Sample_Data   seems like the have some dicoms and a bit of niftis we can playwith    17/06/19
#https://www.researchgate.net/post/What_is_the_easiest_way_to_batch_resize_DICOM_files to down sample dicoms, incase if they're too large  17/06/19
#https://stackoverflow.com/questions/55560243/resize-a-dicom-image-in-python      this one is for python. the one above is for mathlab, i didn't see
#https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python   export mesh to obj   17/06/19

import numpy as np
import pydicom as dicom
import pydicom.pixel_data_handlers.gdcm_handler
import os
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *

data_path = "/Users/apple/Desktop/samples1/"
output_path = working_path = "/Users/apple/Desktop/output/"#todo actually create file
g = glob(data_path + '/*.dcm')

# Print out the first 5 file names to verify we're in the right folder.
#print ("Total of %d DICOM images.\nFirst 5 filenames:" % len(g))
#print ('\n'.join(g[:5]))

#	  
# Loop over the image files and store everything into a list.
# 

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



patient = load_scan(data_path)#hi


#============================choose file=====================================
fileoption = "fullimages_%d.npy"
theoption = 1
if theoption:
	fileoption = "fullimages_%d.npy"
else:
	fileoption = "fullimagesfromnifti_%d.npy"
#============================choose file=====================================



id=0



generateNumPy = 0#flip the switch
if generateNumPy:
	imgs = get_pixels_hu(patient)
#------save to output
	np.save(output_path + fileoption % (id), imgs)

displayHUasGraph = 0
if displayHUasGraph:
	file_used = "..."
	file_used=output_path+fileoption % id
	imgs_to_process = np.load(file_used).astype(np.float64) 

	plt.hist(imgs_to_process.flatten(), bins=50, color='c')
	plt.xlabel("Hounsfield Units (HU)")
	plt.ylabel("Frequency")
	plt.show()

displayTHICCness = 0
if displayTHICCness:
	patient = load_scan(data_path)
	print ("Slice Thickness: %f" % patient[0].SliceThickness)
	print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))


displayImageStack = 0#ill look at this later
if displayImageStack:
	id = 0
	imgs_to_process = np.load(output_path+'fullimages_{}.npy'.format(id))

	def sample_stack(stack, rows=6, cols=6, start_with=10, show_every=3):
		fig,ax = plt.subplots(rows,cols,figsize=[12,12])
		for i in range(rows*cols):
			ind = start_with + i*show_every
			ax[int(i/rows),int(i % rows)].set_title('slice %d' % ind)
			ax[int(i/rows),int(i % rows)].imshow(stack[ind],cmap='gray')
			ax[int(i/rows),int(i % rows)].axis('off')
		plt.show()

	sample_stack(imgs_to_process)


resampling = 0
if resampling:
	#id = 0
	patient = load_scan(data_path)
	print(fileoption)
	fileoption_resamp = fileoption[:-6]+("%d.npy"%id)
	imgs_to_process = np.load(output_path+fileoption_resamp)#'fullimages_{}.npy'+fileoption.format(id)
	def resample(image, scan, new_spacing=[1,1,1]):
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

def make_mesh(image, threshold=-300, step_size=1):

	print ("Transposing surface")
	#print("threshold is " + threshold)
	p = image.transpose(2,1,0)
	
	print ("Calculating surface")
	#https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.marching_cubes_lewiner
	verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold, step_size=step_size, allow_degenerate=True) 
	return verts, faces, norm

def plotly_3d(verts, faces):
	x,y,z = zip(*verts) 
	
	print ("Drawing")
	
	# Make the colormap single color since the axes are positional not intensity. 
#	colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
	colormap=['rgb(236, 236, 212)','rgb(236, 236, 212)']
	
	fig = FF.create_trisurf(x=x,
						y=y, 
						z=z, 
						plot_edges=False,
						colormap=colormap,
						simplices=faces,
						backgroundcolor='rgb(64, 64, 64)',
						title="Interactive Visualization")
	iplot(fig)

def plt_3d(verts, faces):
	print ("Drawing")
	x,y,z = zip(*verts) 
	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111, projection='3d')

	# Fancy indexing: `verts[faces]` to generate a collection of triangles
	mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=1)
	face_color = [1, 1, 0.9]
	mesh.set_facecolor(face_color)
	ax.add_collection3d(mesh)

	ax.set_xlim(0, max(x))
	ax.set_ylim(0, max(y))
	ax.set_zlim(0, max(z))
	ax.set_facecolor((0.7, 0.7, 0.7))#was set_axis_bgcolor
	plt.show()


outid = 5
letsdothis = 1
if letsdothis:
	thresholdinput = input("Please enter HU threshold(int): ")
	#v, f, n = make_mesh(imgs_after_resamp, int(thresholdinput), 1)#350
	#plt_3d(v, f)
	tempnif = np.load(output_path+"fullimagesfromnifti_1.npy")
	v, f, n = make_mesh(tempnif, int(thresholdinput), 1)#350




	f=f+1#not 100% sure why we need this. the mesh looks 'weird' without it    ref >>>>>>   https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python      18/06/19

	thefile = open(output_path + 'OBJs/test%d.obj' % outid, 'w')
	for item in v:
		thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))

	for item in n:
		thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))

	for item in f:
		thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  

	thefile.close()
