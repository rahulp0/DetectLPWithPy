import numpy as np
import cv2

def videoconvertor():
    con,kj=1,3
    finalarea=1
    name="rr.mp4"
    cap = cv2.VideoCapture(name)
    i,pk=1,0
    while(kj):
        toneconarea=0
        ret ,frame = cap.read()
        dummy=frame
        if ret == True:
            p,q,r,s=0,0,2000,1000
            img2 = cv2.rectangle(frame, (p,q), (p+r,q+s),(0,0,255),2)
            frame=frame[0:p+r,600:q+s]
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            if(name=="newone3.MOV"):
                thresh=255-thresh
            _,cont,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for conto in cont:
                area=cv2.contourArea(conto)
                toneconarea+=area
            print toneconarea,i
            if(120000<toneconarea and toneconarea<130000 and ((i%2)==0)  ):
                kj=kj-1
                pk=pk+1
                cv2.imwrite("image/image"+str(i)+".png",dummy)

            i=i+1
            img2 = cv2.resize(img2, (960, 540))                    # Resize image
            cv2.imshow("img2", img2)  
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        else:
            
            break
    print "Number Of Object Detected are :", pk
    cv2.destroyAllWindows()
    cap.release()

videoconvertor()

