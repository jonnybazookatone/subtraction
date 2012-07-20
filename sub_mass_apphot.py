#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_mass_apphot.py |
 ==============

Summary:
        Carry out photometry on all the "best" images found using hotpants.
Usage:
        sub_mass_apphot.py --d . --b r --o object.dat --a apertures --OB OB1_1

	d: directory
	b: band [g,r,i,z,J,H,K], for more than one separate by commas, i.e. -band g,r,i
	o: object of interest co-ordinate file (wcs)
	a: apertures to use for your objects, must be a file, with format of "fap fdap fan", e.g. "1 2 3".
	OB: list of OBs separated by commas
"""

import sys
import glob
from optparse import OptionParser
from sub_apphot import main as sub_apphot

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(directory, bandList, objint, apertures=False, OBList=False):

	# Script outline
	#
	# 1. Find all the OBs
	# 2. Go through all the bands and run the subroutine named sub_apphot.py

	if apertures:
		apfi = open(apertures, "r")
		apfiline = apfi.readlines()
		apfi.close()
		apfiline = apfiline[0].replace("\n","").split(" ")
		fap, fdan, fan = float(apfiline[0]), float(apfiline[1]), float(apfiline[2])
		print "loaded user apertures"
	else:
		fap, fdan, fan = False, False, False
		print "using default apertures"

	# OBs
	#
#	bandList = ['g', 'r', 'i', 'z', 'J', 'H']
	if not OBList:
		OBList = glob.glob("%s/OB*" % directory)
	else:
		OBList = OBList.split(",")
	for band in bandList:
		
		# temp test
		testlcx, testlcy = [], []

		# Output file
		magfile = open("%s/%s_appmag.dat" % (directory, band), "w")

		for OB in OBList:
			
			# Run sub_apphot
			time, time_err, sub_mag, sub_magerr, noise_mag, noise_magerr, subobj, noiseobj = sub_apphot(OB, band, objint, fap=fap, fdan=fdan, fan=fan)

			# Write
			magfile.write("%s %s %s %s %s\n" % (OB, time, time_err, sub_mag, sub_magerr))
			
		# close file
		magfile.close()

if __name__ == "__main__":
  
        parser = OptionParser()
        parser.add_option('--d', dest='directory', help='directory of OBs', default=None)
        parser.add_option('--b', dest='band', help='band', default=None)
        parser.add_option('--o', dest='objint', help='object of interest', default=None)
        parser.add_option('--a', dest='apertures', help='apertures', default=False)
        parser.add_option('--OB', dest='OBList', help='list of OBs', default=False)
        (options, args) = parser.parse_args()

        if options.directory and options.band and options.objint:
		band = options.band.split(",")
                main(options.directory, band, options.objint, options.apertures, options.OBList)
        else:
                print __doc__
                sys.exit(0)

# Mon Dec 12 14:26:58 CET 2011
