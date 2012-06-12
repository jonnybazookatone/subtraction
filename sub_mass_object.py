#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_mass_object.py |
 ==============

Summary:
        Uses the routine sub_make_object.py, which generates an object in an image, given input co-ordinates. This version takes an input file rather than command line options, but can be easily changed.
Usage:
        sub_makemess_object.py --d . --f mkobject.coo --b r

	f: input object file, contains \"ra(deg) dec(deg) magnitude\"
	d: directory path which should be subtraction/remappings/ 
	b: band (seperated by commas; g,r,i,z,....)

"""

import glob
import os
from optparse import OptionParser
from sub_object import make_object

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(directory, coordfile, bandList=None):

	print "----------------"
	print "MASS MAKE OBJECT"
	print "----------------"

	# Get RA, Dec. and Magnitude
	cooFile = open(coordfile, "r")
	cooLine = cooFile.readlines()[0].split(" ")
	cooFile.close()
	ra, dec, magnitude = float(cooLine[0]), float(cooLine[1]), float(cooLine[2])
	print "User coo file: %s" % (coordfile)
	print "-------------"
	print "RA: %s" % (ra)
	print "Dec.: %s" % (dec)
	print "Magnitude: %s" % (magnitude)

	# Make folder list
	print "Given directory: %s" % directory
        OBList = glob.glob("%s/OB*" % directory)
	Missing_list = []
	Skipped_list = []

	# Run over OBs
	for OB in OBList:
		print "#####################"
		for band in bandList:
			print "OB: %s" % (OB)
			print "band: %s" % (band)
			bandpath = "%s/%s" % (OB,band)

			infile = "%s/science_mapping_%s.fits" % (bandpath, band)
			outfile = "%s/science_mapping_%s_mko.fits" % (bandpath, band)

			flag = False
			outflag = False

			if not os.path.exists(bandpath):
				print "This band has no folder, skipping."
				Missing_list.append([OB, band])
				flag = True

			if not os.path.exists(infile):
				print "This has no input fits image, skipping."
                                Missing_list.append([OB, band])
				flag = True

			if os.path.exists(outfile):
				print "There is already an output file, skipping (delete it if you wish to be done again)"
				Skipped_list.append([OB, band])
				outflag = True

			if not flag and not outflag:
				imNew = make_object(infile, ra, dec, magnitude) 

			print "########################"
			print "\n\n"

	print "Total Missing: %d/%d" % (len(Missing_list), len(OBList)*len(bandList))
	if len(Missing_list)>0:
		print ""
		print "Missing List:"
		print "-------------"
		for missing in Missing_list:
			print "OB: %s, band: %s" % (missing[0], missing[1])
		print ""
	print "Total Skipped: %d/%d" % (len(Skipped_list), len(OBList)*len(bandList))

if __name__ == "__main__":

        parser = OptionParser()
        parser.add_option("--d", dest='directory', help='Directory path', default=None)
	parser.add_option("--f", dest="coorfile", help='Co-ordinate file for fake object', default=None)
	parser.add_option("--b", dest="band", help="Band to run on", default=None)
	
        (options, args) = parser.parse_args()

	if options.band:
		band = options.band.split(",")
	else:
		band = options.band

	if options.directory and options.coorfile:
		main(options.directory, options.coorfile, band)
	else:
		print __doc__
# Thu Apr 12 14:52:22 CEST 2012
