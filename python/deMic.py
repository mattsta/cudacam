# Mostly from http://www.endolith.com/wordpress/2009/11/22/a-simple-fastica-example/

from mdp import fastica
from scikits.audiolab import wavread, wavwrite
from numpy import abs, max, array

# Load in the microphone audio files
mic1, fs1, enc1 = wavread('channel1.wav')
mic2, fs2, enc2 = wavread('channel2.wav')
mic3, fs3, enc3 = wavread('channel3.wav')
mic4, fs4, enc4 = wavread('channel4.wav')

# transpose() because MDP expects each COLUMN to be an
# observed data stream.  Each ROW is one observation of that data across
# all data streams.
sources = fastica(array([mic1, mic2, mic3, mic4]).transpose())
 
# The output levels of this algorithm are arbitrary, so normalize them to 1.0.
sources /= max(abs(sources), axis = 0)

(frames, inputs) = sources.shape

# Write one output file for each resulting ICA transform.
for i in range(inputs):
    sourceColumn = sources[:,[i]]  # extract a column from the numpy ndarray
    wavwrite(sourceColumn, "resolved-source%d.wav" % i, fs1, enc1)
