#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                    |
 ================================
| sub_find_bestpants.py |
 =======================

Summary:
        Finds the best subtraction based on the MEAN and STDDEV of the closest object to the object of interest
Usage:
        sub_find_bestpants.py --d . --b 'all = grizJHK' --o objectofinterest.wcs --OB OB1_1,OB1_2
        
        d: directory to run on
        b: band to run on
        o: supply a file called "objectofinterest.dat", of the type "name ra dec" it will find a source closest to this.
	   format of file:   "NAME" "RA" "DEC"
	You can supply a file called "fwhm.dat" within the OB file. The script will use this fwhm rather than calculate its own from SEXtractor.
	OB: list of OBs to run the script on
"""

import os, glob, sys, shutil
from python.imclass.image import imFits, imObject
from optparse import OptionParser

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(directory, bandList, objectOfInt, OBList=None):

	# Script outline
	#
	#	 A. 1. Find all the OB directories of interest
	#	    2. Find all the bands of interest and cube subtractions
	#
	#	 B. 1. In a given band, load an image to be used as the reference and find the Nearest Neighbour (NN) in WCS
	#	    2. Run through each cube image and calculate the statistics of the NN
	#	    3. Once the best image is found, copy it into a master image	


	# A.

        # Make folder list
        print "Given directory: %s" % directory
        if not OBList:
		OBList = glob.glob("%s/OB*" % directory)
        Missing_list = []
        Skipped_list = []
#        bandList = ["g", "r", "i", "z", "J", "H", "K"]

	# Specify the object of interest, e.g. GRB 110918A
        objectOfInterest = imObject()
        
        if objectOfInt:
		print "Using object file, %s" % objectOfInt
                ooifile = open(objectOfInt, "r")
                ooilines = ooifile.readlines()[0].replace("\n", "").split(" ")
                ooifile.close()

                #info = ooilines.split(" ")
                objectOfInterest._Name = ooilines[0]
                objectOfInterest._ra = float(ooilines[1])
                objectOfInterest._dec = float(ooilines[2])
                
        else:
                objectOfInterest._Name = "GRB 110918A"
                objectOfInterest._ra = float(32.53894)
                objectOfInterest._dec = float(-27.10548)

	# Run over bands
	for band in bandList:
		# We want to pick only 1 reference star for each band, so that it is consistent
		# Select this by a "chosen" flag
		chosenflag = False
		# Run over OBs
		for OB in OBList:

			# B. 
			# Specify an object image from the first OB
			print "Loading image."
			ReferenceImage = imFits()
			ReferenceImage._Name = "%s/%s/remcut_%s.fits" % (OB, band, band)

                        # get FWHM and STDEV
                        print "Acquiring background standard deviation and median FWHM."
			ReferenceImage.getBackgroundSTDEV()
			
			fwhmfile = "%s/%s/fwhm.dat" % (OB, band)
			try:
				fwhmf = open(fwhmfile, "r")
				fwhm = float(fwhmf.readlines()[0].replace("\n",""))
				print "FWHM taken from file"
				ReferenceImage._MEDFWHM = fwhm
			except:
				print "Calculating FWHM using SEXtractor"
				ReferenceImage.getMyMedianFWHM()
				

			if not chosenflag:
	                        # Make a temporary object of interest
	                        tempInterest = imObject()
	                        tempInterest.copyObjectProperties(objectOfInterest)

	                        # Make a temporary object of interest
	                        tempInterest = imObject()
	                        tempInterest.copyObjectProperties(objectOfInterest)
				tempInterest._parentimage = ReferenceImage._Name
				tempInterest.findLogicalPosition(write=True)
				#tempInterest.printInfo()
			
				# get FWHM and STDEV
				print "Acquiring background standard deviation and median FWHM."

				# Find the NearestNeighbour
				print "Acquiring stars."
				ReferenceImage.findStars()
				#ReferenceImage.printInfo()
			
				print "Acquiring nearest neighbour to object of interest"
				ClosestNeighbour = ReferenceImage.findNearestNeighbour(tempInterest, rcirc=100, write=True)
				#ClosestNeighbour[0].printInfo()
				ClosestNeighbour[0]._Name = "Closest star"
				ClosestNeighbour[0]._parentimage = ReferenceImage._Name
				# Get the WCS co-ordinates for future image usage
				ClosestNeighbour[0].findWorldPosition(write=True)
				print "Found:"
				ClosestNeighbour[0].printInfo()

				# set chosen flag
				chosenflag = True

			cubeList = glob.glob("%s/%s/sub/cube*" % (OB, band))
			
			# Run over each cube
                        # measure the STDDEV and MEAN of each image utilising IRAF.IMSTAT
                        #
                        #       Keep it in the array [listOfCubeStats]
			ListOfCubeStats = []
		

			for cube in cubeList:

				# load image
				print "Cube: %s" % (cube)
				cubeSubtractedImage = imFits()
				cubeSubtractedImage._Name = "%s/diff_%s.fits" % (cube, band)

				# Get sky STDDEV and FWHM (seeing)
				cubeSubtractedImage.skySTDEV = ReferenceImage._skySTDEV
				cubeSubtractedImage._MEDFWHM = ReferenceImage._MEDFWHM
	
				# Look at a box around object of interest
				tempClosestNeighbour = imObject()
				tempClosestNeighbour.copyObjectProperties(ClosestNeighbour[0])
				tempClosestNeighbour._parentimage = cubeSubtractedImage._Name
				tempClosestNeighbour.findLogicalPosition(write=True)
				cubeSubtractedImage.getObjectStatistics(tempClosestNeighbour)
				#tempClosestNeighbour.printInfo()
				
				# Collect the cube output
				ListOfCubeStats.append(tempClosestNeighbour)
				
			# Find the best cube
			# 	1. Set fake STDDEV and MEAN
			#	2. loop through to find the best
			bestSTDEV, bestMEAN, bestOBJECT = 10000000, 10000000, "None"
			for CubeStats in ListOfCubeStats:

				# Test print
				print CubeStats._STDDEV, CubeStats._MEAN

				if abs(CubeStats._STDDEV) < bestSTDEV: #and abs(CubeStats._MEAN) < bestMEAN:
					bestSTDEV = CubeStats._STDDEV
					bestMEAN = CubeStats._MEAN
					bestOBJECT = CubeStats

			#print "The best object is:"
			#bestOBJECT.printInfo()

			# Copy it to a "best" directory
			bestoutput = "%s/%s/sub/best/" % (OB, band)
			if glob.glob(bestoutput+"*"):
				print "File exists"
				shutil.rmtree(bestoutput)
				print "Deleted"

			shutil.copytree(bestOBJECT._parentimage.replace("diff_%s.fits" % band, ""), bestoutput)
			#print glob.glob(bestoutput+"*")			
			print "Finished OB,band: %s, %s" % (OB,band)
			print "\n\n\n"


if __name__ == "__main__":
                
        parser = OptionParser()
        parser.add_option('--d', dest='directory', help='directory of OBs', default=None)
        parser.add_option('--b', dest='band', help='band', default=None)
        parser.add_option('--o', dest='objint', help='object of interest', default=None)
	parser.add_option('--OB', dest='OBList', help='OB list', default=None)
        (options, args) = parser.parse_args()

        if options.directory and options.band and options.objint:
		band = options.band.split(",")
		OBList = options.OBList.split(",")
                main(options.directory, band, options.objint, OBList)
        else:
                print __doc__
                sys.exit(0)
                

# Thu Dec 8 15:29:33 CET 2011
