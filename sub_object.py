#!/usr/bin/python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_object.py |
 ==============

Summary:
        Generates an object in an image. 
Usage:
        sub_make_object.py --i image.fits --r 28.0 --d 32.0 --m 20

	i: input image
	r: RA (deg)
	d: Dec. (deg)	
	m: Magnitude

        A new output of "imagename"_mko.fits is generated, accompanied by an mkobject.coo file, recording the input values chosen by the user.
"""

import sys
from optparse import OptionParser
from python.imclass.image import imFits, imObject

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def make_object(imageName, ra, dec, magnitude):

	# Inform the user of their choices
	print "User choices:"
	print "------------"
	print "Input image: %s" % (imageName)
	print "RA: %s" % (ra)
	print "Dec.: %s" % (dec)
	print "Magnitude: %s" % (magnitude)

	# Load instance of image object
	scienceImage = imFits()
	scienceImage._Name = imageName

	# Generate an object instance and find out the pixel co-ordinates
	generatedObject = imObject()
	generatedObject._parentimage = scienceImage._Name
	generatedObject._ra = float(ra)
	generatedObject._dec = float(dec)
	generatedObject._appMag = float(magnitude)
	generatedObject.findLogicalPosition(write=False)
	generatedObject.printInfo()

	# Write the user input to file
	cooFile = open("mkobject.coo", "w")
	cooFile.write("%f %f %f" % (generatedObject._pixelx, generatedObject._pixely, generatedObject._appMag))
	cooFile.close()

	# Make the object
	scienceImage.makeObject()

if __name__ == "__main__":

        parser = OptionParser()
	parser.add_option("--i", dest="inputimage", help="Input image name", default=None)
        parser.add_option("--r", dest="ra", help="Right ascension of object", default=None)
        parser.add_option("--d", dest="dec", help="Declination of object", default=None)
        parser.add_option("--m", dest="magnitude", help="Magnitude of the object", default=None)

        (options, args) = parser.parse_args()

	if options.inputimage and options.ra and options.dec and options.magnitude:
		make_object(options.inputimage, options.ra, options.dec, options.magnitude)
	else:
		print __doc__

# Thu Apr 12 14:24:03 CEST 2012
