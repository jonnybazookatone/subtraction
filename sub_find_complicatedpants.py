#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_find_complicatedpants.py |
 ==============

Summary:
        Finds the best subtraction based on the MEAN and STDDEV of the closest object to the object of interest
Usage:
        sub_find_complicatedpants.py -d . -b 'all = grizJHK'
        If you supply a file called "objectofinterest.dat", of the type "name ra dec" it will find a source closest to this. Otherwise it uses a default which will not work.
"""

import os, glob, sys, shutil, getopt
from python.imclass.image import imFits, imObject

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(directory, bandList):

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
        OBList = glob.glob("%s/OB*" % directory)
        Missing_list = []
        Skipped_list = []
#        bandList = ["g", "r", "i", "z", "J", "H", "K"]

	# Specify the object of interest, e.g. GRB 110918A
	objectOfInterest = imObject()
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
				ClosestNeighbour = ReferenceImage.findNearestNeighbour(tempInterest, rcirc=50, write=True)
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
				cubeSubtractedImage.getObjectStatistics(tempClosestNeighbour, multiple=4)
				#tempClosestNeighbour.printInfo()
				
				# Collect the cube output
				ListOfCubeStats.append(tempClosestNeighbour)
				
			# Find the best cube
			# 	1. Set fake STDDEV and MEAN
			#	2. loop through to find the best 3 MEANS and then the bestSTDEV
			bestSTDEV, bestMEAN, bestMEDIAN, bestOBJECT, bestPercentageDiff = 10000000, 10000000, 10000000, False, 10000000


			# Best STDDEV
			for CubeStats in ListOfCubeStats:
				if abs(CubeStats._STDDEV) < bestSTDEV:
					bestSTDEV = abs(CubeStats._STDDEV)

			# Best MEDIAN
			for CubeStats in ListOfCubeStats:
				if abs(CubeStats._MEDIAN) < bestMEDIAN:
					bestMEDIAN = abs(CubeStats._MEDIAN)

			# Best MEAN
			for CubeStats in ListOfCubeStats:
				if abs(CubeStats._MEAN) < bestMEAN:
					bestMEAN = abs(CubeStats._MEAN)

			print "Minimum STDDEV: %f" % bestSTDEV
			print "Minimum MEDIAN: %f" % bestMEDIAN
			print "Minimum MEAN: %f\n" % bestMEAN
			bar = 1.0
			print "STDDEV MEAN MEDIAN"
			for CubeStats in ListOfCubeStats:

				# Test print
				print CubeStats._STDDEV, CubeStats._MEAN, CubeStats._MEDIAN, CubeStats._parentimage

				percentageDiff = abs(1 - ( (CubeStats._MEDIAN/bestMEDIAN) / (bestMEAN/CubeStats._MEAN) )) #/ ( abs(CubeStats._MEDIAN  ) ) 
				if percentageDiff < bestPercentageDiff:
				#if abs(CubeStats._MEDIAN) < (bestMEDIAN+0.1) and abs(CubeStats._MEAN) < bestMEAN+0.1:
					#bestMEDIAN = abs(CubeStats._MEDIAN)
					#bestSTDEV = abs(CubeStats._STDDEV)
					#bestMEAN = abs(CubeStats._MEAN)
					bestOBJECT = CubeStats
					bestPercentageDiff = percentageDiff

			if not bestOBJECT:
				print "No Object found to fit criteria."
				return 0

			print "The best object is:"
			print bestOBJECT._STDDEV, bestOBJECT._MEAN, bestOBJECT._MEDIAN
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
        # Key list
        key_list = "d:b:"
        directory, band = None, None

        # Obtain input
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')

                if flag == "d":
                        directory = arg
                elif flag == "b":
                        if arg == "all":
                                band == ["g", "r", "i", "z", "J", "H", "K"]
                        else:
                                band = [arg]
#               elif flag == "x":
#                       ra = arg
#               elif flag == "y":
#                       dec = arg
                else:
                        print __doc__
                        print sys.exit(0)

        if directory and band:
                print main(directory, band)
        else:
                print __doc__
                sys.exit(0)

# Thu Dec 8 15:29:33 CET 2011
