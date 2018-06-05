
import numpy as np
import time as t
import cv2
import sys
import os
from folder.loadimage import extractImage 

from folder.platedetection import * 
path="/home/rahul/miniproject/cars/"
plates_array = extractImage(path);
print "images are successfully downloaded"
for plate_image in plates_array:
	plate_image.plateSearch()
