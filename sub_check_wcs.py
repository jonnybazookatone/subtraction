#!/usr/bin/python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_check_wcs.py |
 ==============

Summary:
        
Usage:
       python sub_check_wcs.py -d dir
"""

import python.subtraction.pyremap.wcsremap as remap
import os, re, glob, sys, getopt

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(PATH):

	print "--------------"
	print "WCSREMAP CHECK"
	print "--------------"

	logger = {}
	logger['Info'] = []

	remapping_DIR = "%s/remappings" % PATH
	if not os.path.exists(remapping_DIR):
		logger['Info'].append("remappings folder does not exist in the directory given")
		sys.exit(0)

	# Bands
	bandList = ["g", "r", "i", "z", "J", "H", "K"]

	# OB in the remapping folder
	OBList = glob.glob("%s/OB*" % remapping_DIR)

	# Inform user
	print "OB Mapping Information"
	print "######################"
	print "Number of OBs: %f" % len(OBList)
	print "OBs: %s" % OBList
	print "######################"
	print ""
	print "Individual OB information"
	print "#########################"

	# Check each folder
	Missing_list = []

	for OB in OBList:
		band_inc = 0
		for band in bandList:
			bandpath = "%s/%s/input_remapping.fits" % (OB,band)
			print "Bandpath: %s" % bandpath
			if os.path.exists(bandpath):
				band_inc = band_inc + 1
			else:
				print "!!!MISSING REMAPPING!!!"
				print "OB: %s" % (OB)
				print "Band: %s" % (band)
				Missing_list.append([OB, band])
			print ""
				
		if band_inc == len(bandList):
			print "OB: %s" % (OB)
			print "All bands have remappings"
		band_inc = 0

	if len(Missing_list)>0:
		print "Final missing list:"
		for missing in Missing_list:
			print "OB: %s, band: %s" % (missing[0], missing[1])

	else:
		print "Nothing missing"

	
	return(Missing_list)

if __name__ == "__main__":

	# Key list for input & other constants, stupid final colon
        key_list = 'd:'

        # Check input
        try:
                x=sys.argv[1]
        except:
                print Usage 
                sys.exit(0)

        # Take the input & sort it out
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')
                
		if flag == "d":
			directory = arg  
		else:
			print Usage
			sys.exit(0)

	Missing_list = main(directory)
