cudacam: experiments in cuda, opencv, and kinect under Linux
============================================================

Status
------
This is a playground.  Things will probably work if you
install enough dependencies.


Things
------
To use all the examples here, install these dependencies.  Most can be `pip` installed.

* numpy - http://numpy.scipy.org/
* freenect - https://github.com/OpenKinect/libfreenect
* cv2 - http://opencv.willowgarage.com/
* mdp - http://mdp-toolkit.sourceforge.net/
* scikits.audiolab (requires libsndfile)
* CUDA Toolkit 4.0 - http://developer.nvidia.com/cuda-toolkit-40
  * libcudart.so
  * libnpp.so

Future dependencies:

* Theano
* PyCUDA
* pypy when numpy support is more complete


Hints
-----
Performance will vary wildly depending on your setup.
Compile opencv yourself to get maximum performance (do not trust pre-packaged versions):

    mkdir build
    cmake -DWITH_OPENNI=yes -DBUILD_EXAMPLES=yes -DWITH_TBB=yes -DWITH_IPP=yes -DIPP_H_PATH=/opt/intel/ipp/include/ ..

* OPENNI can come from https://github.com/OpenNI/OpenNI
* IPP can come from http://software.intel.com/en-us/articles/non-commercial-software-download/ (tip: the registration forms accepts fake credentials).
* TBB can come from your distro or from http://threadingbuildingblocks.org/file.php?fid=77

After I enabled TBB (from distro) and IPP (downloaded and installed manually), the
haar face detector doubled in speed (=> video frame rate doubled).
