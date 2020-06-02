# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2



class Detector:
    
    isadjusted=False
    yetajusted=False    
    otherval=False
    base = None
    count=0
    countc=0
    def TurnOnVideo(self):
                  
        camera=cv2.VideoCapture(0)
        while True:
            ncontour=0              
            # grab the current frame and initialize the occupied/unoccupied
            # text
            (grabbed, frame) = camera.read()            
            
            bigcontour=None
            text = "Empty scene (Frames: "+str(self.countc)+" )"+str(self.yetajusted)
            
            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if not grabbed:
                break

            # resize the frame, convert it to grayscale, and blur it
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            original=gray
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # if the first frame is None, initialize it	
            self.adjuster(gray)				
                    
            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(self.base, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            
            # dilate the thresholded imagebaseill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)    
            (some,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            height,width,channels = frame.shape
            
            for x in range(1,16):                
                frame = cv2.line(frame , (int(width/15)*x, 0), (int(width/15)*x, height), (0, 255, 0), 2)
                #print ("Lineas "+str(int(width/15)*x))
            # loop over the contours       
            texta=""                     
            for c in cnts:
                text="Object"
                ncontour=ncontour+1
                # if the contour is too small, ignore it                                
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                
                self.count=self.count+1                
                if x>45:
                    if x>84:
                        if x>126:
                            if x>168:
                                if x>210:
                                    if x>252:
                                        if x>294:
                                            if x>336:
                                                if x>378:
                                                    if x>420:
                                                        if x>462:
                                                            if x>504:
                                                                if x>546:
                                                                    if x>588:
                                                                        if x>630:
                                                                            texta="15"
                                                                        else:
                                                                            texta="14"
                                                                    else:
                                                                        texta="13"
                                                                else:
                                                                    texta="12"
                                                            else:
                                                                texta="11"
                                                        else:
                                                            texta="10"
                                                    else:
                                                        texta="9"
                                                else:
                                                    texta="8"
                                            else:
                                                texta="7"
                                        else:
                                            texta="6"
                                    else:
                                        texta="5"
                                else:
                                    texta="4"
                            else:
                                texta="3"
                        else:
                            texta="2"
                    else:
                        texta="1"
                
                if self.isadjusted==True:
                    if y>300:
                        print("Height:{}".format(y))  
                        self.countc = self.countc +1 
                        he,wi = original.shape
                        if x+w+3<wi:                            
                            outt = original[x:x+w+5, y-10:y+h]
                            cv2.rectangle(frame, (x, y-10), (x + w+5, y + h), (255, 0, 0), 2)
                        else:
                            outt = original[x:x+w, y:y+h]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        bigcontour=outt 
                        cv2.imwrite('Catched/{}.png'.format(self.countc),outt)
                        print(self.countc)
                else:
                    self.countc=0

                
                #print("x: ",x,"\ny: ",y,"\nw: ",w,"\nh: ",h)                  
            if ncontour>10:
                self.yetajusted=False            
            # draw the text and timestamp on the frame
            cv2.putText(frame, " {} {}".format(text,texta), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                
            # show the frame and record if the user presses a key	
            
            
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
            cv2.imshow("Security Feed", frame)
            key = cv2.waitKey(1) & 0xFF
            
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                print("Aasd")
                break
            
        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()                

        return 
        
    def adjuster(self,gray):
        ctemp=self.countc
        if self.base is None:
            self.base=gray

        if self.count > 50 and self.yetajusted==False:        
            print("adjusting")
            self.yetajusted=True      					    	
            self.isadjusted=True	
            self.base = gray
            cv2.imwrite('Base.png',gray)	
            self.count=0                       	            	
            self.countc=0
        if self.yetajusted==True:
            self.countc=ctemp
        return

def main():
    detector=Detector()    
    detector.TurnOnVideo()
    pass

if __name__ == '__main__':
    main()