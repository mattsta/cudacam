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

    m = get_video() #cv.QueryFrame(capture)

cascade = cv.Load(base + '../priv/haarcascade_frontalface_alt.xml')
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
              cv.CV_HAAR_DO_CANNY_PRUNING, (50, 50))

    if faces:
        print 'face detected!'
        for (x, y, w, h), n in faces:
            cv.Rectangle(image, (x, y), (x+w, y+h),
                         cv.RGB(0, 255, 0), 3, 8, 0)


while True:
    frame = get_video()

#    cv.Flip(frame, None, 1)
    detect(frame)
    cv.ShowImage("Bob", frame)

    k = cv.WaitKey(10)
