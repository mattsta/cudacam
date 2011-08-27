# Mostly from:
# http://openvidia.sourceforge.net/index.php/OpenVIDIA/python

import numpy as np
import freenect
import cv
import frame_convert
from ctypes import *

cudart = CDLL("libcudart.so")
npp = CDLL("libnpp.so")

class NppiSize(Structure):
    _fields_ = [("width", c_int),
                ("height", c_int)]

thresh_type = c_ubyte * 3

def get_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])
def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

img = cv.CreateMat(480, 640, cv.CV_8UC4)
npp.nppsMalloc_8u.restype = POINTER(c_char)
d_a = npp.nppsMalloc_8u(648*480*4)
d_b = npp.nppsMalloc_8u(648*480*4)
roi = NppiSize()
roi.width = 640
roi.height = 480

def repeat():
    m = get_video() #cv.QueryFrame(capture)
    # convert the image from RGB to RGBA for thresholding
    cv.CvtColor(m, img, cv.CV_RGB2RGBA)

    # convert the cv image into a array and get a data pointer    (h_a)
    a = np.fromstring(img.tostring(),dtype='uint8',count=img.width*img.height*4)
    a.shape = [img.height, img.width, 4]
    h_a = a.ctypes.data_as(POINTER(c_char))

    # send to GPU
    cudart.cudaMemcpy(d_a, h_a, 480*640*4, 1)
    # NPP thresholding
    npp.nppiThreshold_8u_AC4R(d_a , c_int(640*4),
                    d_b, c_int(640*4), roi, thresh_type(128,128,128), 0)
    # readback from GPU
    cudart.cudaMemcpy(h_a, d_b, 480*640*4, 2)

    # copy result into the OpenCV image structure
    cv.SetData(img, a.tostring(), 640*4)

    # display the image
    cv.ShowImage("NPP Python", img)
    c = cv.WaitKey(5)

while True:
    repeat()
