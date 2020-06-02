# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2


# construct the argument parser and parse the arguments
count=0
countc=0
isadjusted=False
yetajusted=False
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
 
# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])
 
# initialize the first frame in the video stream
firstFrame = None

a=0
# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied (Frames: "+str(countc)+" )"+str(yetajusted)
 
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break
 
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	cv2.imwrite('Base.png',gray)
	# if the first frame is None, initialize it	
	if count>50:				
		yetajusted=True
	if firstFrame is None or count > 50:     					    	
		isadjusted=True		
		firstFrame = gray	
		count=0				
		continue	
	if isadjusted==True:
		if yetajusted==False:
			countc=0				
		
	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)    
	(some,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
	# loop over the contours
	
	for c in cnts:
		# if the contour is too small, ignore it
		countc = countc +1
		if cv2.contourArea(c) < args["min_area"]:
			continue		
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)		
		count=count+1	
		if isadjusted==True:
    			cv2.imwrite('Catched/{}.png'.format(countc),gray)	
		else:
			countc=0
		if count>50:
			text = "Occupied (Adjusting camera)"
		else:
			text = "Occupied"
		outt = frame[x:x+w, y:y+h]
		print("x: ",x,"\ny: ",y,"\nw: ",w,"\nh: ",h)
		a=a+1
		outputt='Out'+str(a)+'.png'
		#cv2.imwrite(outputt,outt)

        # draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
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