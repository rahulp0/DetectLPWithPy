import numpy as np
import cv2
import math
from folder.platedetection import *
def videoconvertor():
    plates_array=[]
    found,i=0,0
    finalarea=1
    name="kk.mp4"
    cap = cv2.VideoCapture(name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    med=math.trunc(fps/2)
    i,pk=1,0
    while(1):
        toneconarea=0
        ret ,frame = cap.read()
        dummy=frame
        if ret == True:
            frame=cv2.resize(frame, (1100,600));
            img=frame
            imgBlurred = cv2.GaussianBlur(img, (5,5), 0)
            gray = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)
            ret2,threshold_img = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            #element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3, 3))#calibrated for rr.mp4
            element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3, 3))#calibrated for kk1.mp4 
            #element = cv2.getStructuringElement(shape=cv2.MORPH_CROSS, ksize=(1,1))#calibrated for kk.mp4
            #dilated = cv2.dilate(threshold_img,element, iterations=15)#varies from 1-3 #calibrated for kk.mp4
            dilated = cv2.dilate(threshold_img,element, iterations=5)#varies from 1-3 kk.mp4 
            thresh=dilated
            _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for con in contours:
                area=cv2.contourArea(con)
                [x, y, w, h] = cv2.boundingRect(con)
                image=frame
                #if w>50 and w<350 and  h>30 and h<250 and y>100 and x>50:#condition is to be Verified to kk.mp4
                if w>70 and w<350 and  h>30 and h<250 and y>100 and x>50:#condition is to be Verified to kk1.mp4
                #if w>70 and w<100 and  h>30 and h<60 and y>200 and x>100:#condition is to be Verified to rr.mp4
                    img2=cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),0);
                    found=1;
                else:
                    img2=image
            if(found):
                    plateObject=Detect_Plate(frame,i)
                    i=i+1;
                    plates_array.append(plateObject)
                    #cv2.imwrite("../../cars/car"+str(w)+".png",frame)
            img2 = cv2.resize(frame, (1100,600))                    # Resize image
            cv2.imshow("img2", img2)  
            k = cv2.waitKey(1) & 0xee
            if k == 27:
                break

        else:
            
            break
    cv2.destroyAllWindows()
    cap.release()
    for plate_image in plates_array:
        plate_image.plateSearch()
videoconvertor()
