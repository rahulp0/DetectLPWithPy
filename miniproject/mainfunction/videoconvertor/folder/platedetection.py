import cv2;
import numpy as np;
from copy import deepcopy, copy;
import logging;
from PIL import Image;
import pytesseract;
import re

class Detect_Plate:
	def __init__(self,image,n):
		self.original_Image=image;
		self.i=n;
		self.n=0;
		self.inve=None;
		self.plate_Image=None;
		self.gray_Image=None;
		self.noise_Image=None;
		self.binary_Image=None;
		self.Inverted_Image=None;
		self.plate_Image=[];
		self.contplate=[];
		self.a=[];
		self.charoi=[];
		self.plate_number="";
		self.m=[];
		pass
	def grayConversion(self,image):
		return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);
	def plateSearch(self):
		
		self.findContour();
		self.cropPlate();
		self.findCharContour()
		self.tensorflowdetection()
	def findContour(self):
		
		image=deepcopy(self.original_Image);
		#org[i]=image;

		self.gray_Image=self.grayConversion(image);
		
		blur = cv2.GaussianBlur(self.gray_Image,(1,1),0)
		
		ret,self.binary_Image = cv2.threshold(blur,0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU);  
		
		self.binary_Image=255-self.binary_Image
		kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,1)) #2,2
		dilated = cv2.dilate(self.binary_Image, kernel, iterations=5)#vary from 1-3 
		
		_,contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

		w,h,x,y= 0,0,0,0;
		im=None
		for con in contours:
			area=cv2.contourArea(con)
			[x, y, w, h] = cv2.boundingRect(con)
			#if w>70 and w<100 and  h>30 and h<60 and y>200 and x>100:#condition is to be Verified to rr.mp4
			#if w>50 and w<350 and  h>30 and h<250 and y>100 and x>50:#condition is to be Verified kk.mp4
			if w>50 and w<350 and  h>30 and h<250 and y>100 and x>50:#condition is to be Verified kk.mp4 and kk1.mp4
				self.a.append([x,y,w,h])
				#im=cv2.rectangle(self.original_Image,(x,y),(x+w,y+h),(255,255,255),0);
		#cv2.imwrite("/home/rahul/miniproject/imagecontour/con"+str(self.i)+".png",im)       					
		return True;
	def cropPlate(self):
		for ia in range(0,len(self.a)):
			[x,y,w,h] = self.a[ia];
			im=self.original_Image
			plate=im[y:y+h,x:x+w]
			self.plate_Image.append(plate)
			#cv2.imwrite("/home/rahul/miniproject/plates/"+str(self.i)+"con"+str(ia)+".png",plate)
		return True;
	def findCharContour(self):
		w,h,x,y= 0,0,0,0;global plateimage
		#print self.i,len(self.plate_Image)
		for ll in range(0,len(self.plate_Image)):
			img=self.plate_Image[ll]
			dummy=img
			img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			ret,img = cv2.threshold(img,117,255,0)
			skel=255-img
			element=cv2.getStructuringElement(cv2.MORPH_CROSS,(1,1))
			skel=cv2.erode(skel,element)
			#cv2.imwrite("/home/rahul/miniproject/conplates/"+str(self.i)+"con.png",skel)
			_,contours, hierarchy = cv2.findContours(skel, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

			w,h,x,y,ff= 0,0,0,0,0;
			im=None
			for con in contours:
				area=cv2.contourArea(con)
				[x, y, w, h] = cv2.boundingRect(con)
				if(w>7 and w<20 and h>10 and h<20):
					ff=ff+1;
			if(ff>1 and ff<10):
				#print ff,self.i,ll
				self.contplate.append(dummy)
				#cv2.imwrite("/home/rahul/miniproject/selectedplates/"+str(self.i)+"con"+str(ll)+".png",dummy)
		return True
	def tensorflowdetection(self):
		for ll in range(0,len(self.contplate)):
			img = cv2.resize(self.contplate[ll],(400,100))
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
			#print text;
			tt=re.sub('[^A-Za-z0-9]+', '', text);
			kk=""
			text=text.split()
			try:
				text="".join([str(item) for item in text])
			except:
				text=""
			if((len(text)>7 and len(text)<12) or (len(tt)>7 and len(tt)<12)):
				kk=re.search('[a-z|A-Z]{2}[0-9]{2}[a-z|A-Z]{1}[0-9]{4}',text)
				text="".join([str(item) for item in text])
				kk=re.search('[a-z|A-Z]{2}[0-9]{2}[a-z|A-Z]{1}[0-9]{4}',tt)
				try:
					text=kk.group(0)
				except:
					text=""
				if(text!=""):
					print "\n******Number plate Character******"
					print "car number:",ll," Plate number:",text
					cv2.imwrite("/home/rahul/miniproject/selectedplates/"+text+".png",self.original_Image)
					print "************************************"
			else:
				pass
				
		cv2.waitKey(0)
		cv2.destroyAllWindows()
