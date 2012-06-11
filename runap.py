#!/usr/bin/env python
"""Default python script layout."""

from imclass.image import imFits, imObject
from optparse import OptionParser

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  ""
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(band, image, ra, dec):

        # Object of Interest
        objectOfInterest = imObject()
        objectOfInterest._Name = "GRB110918A"
	objectOfInterest._ra = float(ra)
	objectOfInterest._dec = float(dec)
#	objectOfInterest._ra = 32.538645
#	objectOfInterest._dec = -27.105838
        #objectOfInterest._ra = 32.53894
        #objectOfInterest._dec = -27.10548

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
        InitialImage._Name = image 
        InitialImage.getBackgroundSTDEV()
        InitialImage.getMyMedianFWHM()

	# 1 pixel is 0.6"
	try:
		pixelscale = abs(InitialImage.getHeader("CD1_1"))*3600.0
	except:
		pixelscale = abs(InitialImage.getHeader("CDELT1"))*3600.0


        objectOfInterest.setAps(fap=1, fdan=2.0, fan=3.0, scale=(InitialImage._MEDFWHM/pixelscale))

	objectOfInterest._parentimage = InitialImage._Name
	objectOfInterest.findLogicalPosition(write=True)

	InitialImage.runApperturePhotometryOnObject(objectOfInterest)
	objectOfInterest.printInfo()


if __name__ == "__main__":

        parser = OptionParser()
        parser.add_option('--band', dest='band', help='Image band filter', default=None)
	parser.add_option('--image', dest='image', help='Image', default=None)
	parser.add_option('--ra', dest='ra', help='ra', default=None)
	parser.add_option('--dec', dest='dec', help='dec', default=None)
	
        (options, args) = parser.parse_args()

	if options.band and options.image and options.ra and options.dec:
		main(options.band, options.image, options.ra, options.dec)
	else:
		print "usage: runap.py --band r --image diff_r.fits --ra 30.0 --dec -10.0"

# Mon Apr 23 16:04:03 CEST 2012
