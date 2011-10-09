# A combination of:
# http://opencv.willowgarage.com/documentation/python/objdetect_cascade_classification.html#haar-feature-based-cascade-classifier-for-object-detection
# and
# http://blog.jozilla.net/2008/06/27/fun-with-python-opencv-and-face-detection/ (old)

import numpy as np
import freenect
import cv2.cv as cv
import frame_convert
import sys
import os

base = os.path.dirname(sys.argv[0])

def get_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])
def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

cascade = cv.Load(base + '../priv/haarcascade_frontalface_alt.xml')

# expand found face height boundary by expansion:
expansion = 10
height_offset=15
FRAME_WIDTH=320
FRAME_HEIGHT=240

def detect(image):
    image_size = cv.GetSize(image)

    # to grayscale
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_RGB2GRAY)

    # equalize
    cv.EqualizeHist(grayscale, grayscale)

    # detections
    faces = cv.HaarDetectObjects(grayscale, cascade,
              cv.CreateMemStorage(), 1.2, 2,
              cv.CV_HAAR_DO_CANNY_PRUNING, (15, 15))

    if faces:
        print 'face detected!'
        for faceN, ((x, y, w, h), n) in enumerate(faces):
            y_offset = y - height_offset
            h_expanded = h + expansion
            h_expanded_offset = h_expanded + height_offset
            if y_offset + h_expanded_offset > FRAME_HEIGHT:
                h_expanded_offset = (y_offset + h_expanded_offset) - FRAME_HEIGHT

            if y_offset < 0:
                y_offset = 0

            windowName = "Face %d" % faceN
            sub = cv.GetSubRect(image, (x, y_offset, w, h_expanded_offset))
            grow = cv.CreateMat(h_expanded*4, w*4, cv.CV_8UC3)
            cv.Resize(sub, grow)
            print "Showing for ", windowName
            cv.ShowImage(windowName, grow)
#                cv.ShowImage("Face at (%d, %d)" % (x, y), grow)
            cv.Rectangle(image, (x, y-height_offset), (x+w, y+h+expansion),
                         cv.RGB(0, 255, 0), 3, 8, 0)



while True:
    frame = get_video()

    # scale down the 640x480 kinect to half size for quicker processing
    shrunk = cv.CreateMat(FRAME_HEIGHT, FRAME_WIDTH, cv.CV_8UC3)
    cv.Resize(frame, shrunk)

#    cv.Flip(frame, None, 1)
    detect(shrunk)
    cv.ShowImage("Bob", shrunk)

    k = cv.WaitKey(10)
