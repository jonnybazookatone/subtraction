#!/usr/bin/python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_appphot.py |
 ==============

Summary:
        Calculates the photometry for your given object, both in the normal images and the noise images (for errors).
Usage:
        sub_apphot.py -d directory -b band -o objectfile
"""

import sys, os, shutil, glob, getopt

from python.imclass.image import imFits, imObject

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(directory, band, objectfile):

	# Open and parse objectfile
	objectOfInterest = imObject()
	if objectfile:
		objintfile = open(objectfile, "r")

		obji = objintfile.readlines()[0].replace("\n", "").split(" ")
		objectOfInterest._Name = obji[0]
		objectOfInterest._ra = float(obji[1])
		objectOfInterest._dec = float(obji[2])
		objintfile.close()
	else:
		print __doc__
		sys.exit(0)

	#objectOfFakeness = imObject()
	#objectOfFakeness._Name =
	#objectOfFakeness._ra =
	#objectOfFakeness._dec =

        # Script outline
        # 1. Initial image
        #
        #       Acquire the FWHM and background STDDEV from the original uncut image
        #
        # 2. Normal Image
        #
        #       Load the image and take photometry at the given position
        #
        # 3. Noise Image
        #
        #       Do the same as on the normal image
        #
        # 4. Save the output in a file

	# Normal image
	InitialImage = imFits()
	InitialImage._Band = band
        InitialImage._Name = "%s/%s/remcut_%s.fits" % (directory, InitialImage._Band, InitialImage._Band)
	InitialImage.getBackgroundSTDEV()
	InitialImage.getMyMedianFWHM()

	# SubtractedImage
	SubtractedImage = imFits()
	SubtractedImage._Band = band
	SubtractedImage._Name = "%s/%s/sub/best/diff_%s.fits" % (directory, SubtractedImage._Band, SubtractedImage._Band)
	SubtractedImage._skySTDEV = InitialImage._skySTDEV
	SubtractedImage._MEDFWHM = InitialImage._MEDFWHM

	SubObject = imObject()
	SubObject._parentimage = SubtractedImage._Name
	SubObject.copyObjectProperties(objectOfInterest)
	SubObject.findLogicalPosition(write=True)

	# Noise image
	NoiseImage = imFits()
	NoiseImage._Band = band
	NoiseImage._Name = "%s/%s/sub/best/diff_%s_noise.fits" % (directory, NoiseImage._Band, NoiseImage._Band)

	# Noise Squared
	NoiseSquaredImage = imFits()
	NoiseSquaredImage._Band = band
	NoiseSquaredImage._Name = NoiseImage.squareMyself()
	NoiseSquaredImage._skySTDEV = InitialImage._skySTDEV
	NoiseSquaredImage._MEDFWHM = InitialImage._MEDFWHM

	NoiseObject = imObject()
	NoiseObject._parentimage = NoiseSquaredImage._Name
	NoiseObject.copyObjectProperties(objectOfInterest)
	NoiseObject.findLogicalPosition(write=True)

	# Photometry
	#
	# Normal image
	#
	SubtractedImage.runApperturePhotometryOnObject(SubObject)
	
	#
	# Noise image 
	#
	NoiseSquaredImage.runApperturePhotometryOnObject(NoiseObject)

	return SubObject._midMJD, SubObject._appMag, SubObject._appMagErr, NoiseObject._appMag, SubObject._appMagErr, SubObject, NoiseObject

if __name__ == "__main__":

	# Key list
	key_list = "d:b:o:"
	directory, band, obji = None, None, None

	# Obtain input
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')

                if flag == "d":
                        directory = arg
                elif flag == "b":
			band = arg
		elif flag == "o":
			obji = arg
#		elif flag == "x":
#			ra = arg
#		elif flag == "y":
#			dec = arg
                else:
                        print __doc__
                        sys.exit(0)

	if directory and band:
		print main(directory, band, obji)
	else:
		print __doc__
		sys.exit(0)
# Mon Dec 12 13:39:20 CET 2011
