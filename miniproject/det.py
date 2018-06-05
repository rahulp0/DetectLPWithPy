import cv2
import numpy as np
import pytesseract
import os
import re
folder="/home/rahul/miniproject/selectedplates/"
i=0

for image_filename in os.listdir(folder):
	#print "Loading image:", image_filename
	image_file = cv2.imread(folder+image_filename)
	img = cv2.resize(image_file,(400,100))
	imag=img
	img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	coords = np.column_stack(np.where(img > 0))
	angle = cv2.minAreaRect(coords)[-1]
	if angle < -45:
		angle = -(90 + angle)
	else:
		angle = -angle
	(h, w) = imag.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(imag, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
	#cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	img=rotated
	img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	element=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	img=cv2.dilate(img,element)
	skel=img
	text = pytesseract.image_to_string(skel)
	kk=""
	text=text.split()
	try:
		text="".join([str(item) for item in text])
	except:
		text=""
	if(len(text)>7 and len(text)<12):
		print "\n******Number plate Character******"
		kk=re.search('[a-z|A-Z]{2}[0-9]{2}[a-z|A-Z]{1}[0-9]{4}',text)
		text="".join([str(item) for item in text])
		try:
			text=kk.group(0)
		except:
			text=""
		if(text!="")
			print "car number:",i," Plate number:",text
			print "************************************"
	else:
		pass
			
	i=i+1		
cv2.waitKey(0)
cv2.destroyAllWindows()
