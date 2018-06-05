import cv2
import os
import logging
import numpy as np
from folder.platedetection import *

#plate=Detect_Plate();
""" Loads all the images of cars from `/images/cars/` """
def extractImage(folder):
	plates_array = []
	i=1
	for image_filename in os.listdir(folder):
		print "Loading image ",i,":", image_filename
		image_file = cv2.imread(folder+image_filename)
		plateObject=Detect_Plate(image_file,i)
		plates_array.append(plateObject)
		i=i+1
	print "\n"
	return plates_array
