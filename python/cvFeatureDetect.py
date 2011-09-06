# A combination of:
# cvFaceDetect.py and GoodFeaturesToTrack from http://opencv.willowgarage.com/documentation/python/cookbook.html

import numpy as np
import freenect
import cv2.cv as cv
import frame_convert
import sys
import os

def get_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])
def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

SCALE_X = 320
SCALE_Y = 240
temp_eigen = cv.CreateMat(SCALE_Y, SCALE_X, cv.CV_32FC1)
temp_image = cv.CreateMat(SCALE_Y, SCALE_X, cv.CV_32FC1)

def features(image):
    image_size = cv.GetSize(image)

    # to grayscale
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_RGB2GRAY)

    # equalize
    cv.EqualizeHist(grayscale, grayscale)

    # detections
    features = cv.GoodFeaturesToTrack(grayscale, temp_eigen, temp_image,
                                      10, 0.04, 1.0, useHarris = True)

    if features:
        for (x, y) in features:
            cv.Rectangle(image, (x, y), (x+4, y+4),
                         cv.RGB(0, 255, 0), 3, 8, 0)


while True:
    frame = get_video()

    # scale down the 640x480 kinect to half size for quicker processing
    shrunk = cv.CreateMat(SCALE_Y, SCALE_X, cv.CV_8UC3)
    cv.Resize(frame, shrunk)

#    cv.Flip(frame, None, 1)
    features(shrunk)
    cv.ShowImage("Bob", shrunk)

    k = cv.WaitKey(10)
