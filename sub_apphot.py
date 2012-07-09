#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.1                   |
 ================================
| sub_appphot.py |
 ==============

Summary:
        Calculates the photometry for your given object, both in the normal images and the noise images (for errors).
Usage:
        sub_apphot.py -d directory -b band -o objectfile

	if a file called "fwhm.dat" exists within the image folder, it will use this as the FWHM. Format, "FWHM", if not there, SExtractor is used.
"""

import sys
from optparse import OptionParser

from python.imclass.image import imFits, imObject

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(directory, band, objectfile, fap=False, fdan=False, fan=False):

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

        fwhmfile = "%s/%s/fwhm.dat" % (directory, band)
        try:
		fwhmf = open(fwhmfile, "r")
		fwhm = float(fwhmf.readlines()[0].replace("\n",""))
		print "FWHM taken from file"
		InitialImage._MEDFWHM = fwhm
	except:
		print "FWHM calculated by SExtractor"
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

	# Photometry
	#
	# Normal image
	#
	fwhm = InitialImage._MEDFWHM
	if fap and fdan and fan:
		print "User defined apertures"
		print ""
		print "fap fdan fan"
		print "%f %f %f" % (fap, fdan, fan)
		fap = fap
		fdan = fdan
		fan = fan
	else:
		fap = fwhm
		fdan = 2*fwhm
		fan = 2.2*fwhm
		
	SubObject.setAps(fap=fap, fdan=fdan, fan=fan, scale=1)
	SubObject.getAps(write=True)
	SubtractedImage.runApperturePhotometryOnObject(SubObject)
	#
	# Noise image 
	#
	NoiseImage = imFits()
	NoiseImage._Band = band
	NoiseImage._Name = "%s/%s/sub/best/diff_%s_noise.fits" % (directory, NoiseImage._Band, NoiseImage._Band)

	# Noise Squared
	NoiseSquaredImage = imFits()
	NoiseSquaredImage._Band = band
	NoiseSquaredImage._Name = NoiseImage.squareMyself()
	#NoiseSquaredImage._skySTDEV = InitialImage._skySTDEV
	NoiseSquaredImage.getBackgroundSTDEV()
	NoiseSquaredImage._MEDFWHM = InitialImage._MEDFWHM

	NoiseObject = imObject()
	NoiseObject._parentimage = NoiseSquaredImage._Name
	NoiseObject.copyObjectProperties(objectOfInterest)
	NoiseObject.setAps(fap=fap, fdan=fdan, fan=fan, scale=1)
	NoiseObject.findLogicalPosition(write=True)
	
	NoiseSquaredImage.runApperturePhotometryOnObject(NoiseObject)
	subError = NoiseSquaredImage.calculateError(SubObject, NoiseObject)

	InitialImage.loadHeader()
	#timeError = InitialImage.getHeader("EXPTIME")
	
	# Set the subtracted error from the noise image and not the error from the subtracted image
	SubObject._appMagErr = subError
	
	return SubObject._midMJD, SubObject._midMJDErr, SubObject._appMag, SubObject._appMagErr, NoiseObject._appMag, SubObject._appMagErr, SubObject, NoiseObject

if __name__ == "__main__":


        parser = OptionParser()
        parser.add_option('-d', dest='directory', help='directory of OBs', default=None)
        parser.add_option('-b', dest='band', help='band', default=None)
        parser.add_option('-o', dest='objint', help='object of interest', default=None)
        parser.add_option('-a', dest='apertures', help='apertures', default=None)
        (options, args) = parser.parse_args()

	if options.directory and options.band and options.objint:
	  
		if options.apertures:
			apfil = open(options.apertures, "r")
			apf = apfil.readlines()
			apfil.close()
			aps = apf[0].replace("\n","").split(" ")
			fap, fdan, fan = float(aps[0]), float(aps[1]), float(aps[2])
		
			print main(options.directory, options.band, options.objint, fap=fap, fdan=fdan, fan=fan)
		else:
			print main(options.directory, options.band, options.objint)
	else:		
		print __doc__
		sys.exit(0)
# Mon Dec 12 13:39:20 CET 2011
