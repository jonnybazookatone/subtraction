#!/usr/bin/python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_clean_pants.py |
 ==============

Summary:
        
Usage:
       python sub_clean_pants.py -d dir
"""

import python.subtraction.pyremap.wcsremap as remap
import os, re, glob, sys, getopt, shutil

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

Usage = """python sub_clean_pants.py -d dir"""

def main(directory):

	print "#############"
	print "PYPANTS CLEAN"
	print "#############"

	logger = {}
	logger['Info'] = []

	flag = False
	while flag == False:
		answer = raw_input("Are you sure you want to delete ALL hotpants diff_[band].fits files?: y/n\n")
		if answer == "y":
			flag = True
			print "Cleaning pants."
		elif answer == "n":
			print "Aborting pants clean."
			sys.exit(0)

	# Bands
	bandList = ["g", "r", "i", "z", "J", "H", "K"]

	# OB in the remapping folder
	OBList = glob.glob("%s/OB*" % directory)

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

	deleted_fold = 0
	nodeleted = 0

	for OB in OBList:
		band_inc = 0
		for band in bandList:
			sub_path = "%s/%s/sub" % (OB, band)
			print "OB: %s, band: %s" % (OB, band)

			if os.path.exists(sub_path):
				print "subtraction folder existed, deleted."
				shutil.rmtree(sub_path)
				deleted_fold = deleted_fold + 1
				
			else:
				print "no subtraction folder to remove."
				nodeleted = nodeleted + 1

	print ""
	print "Total deleted: %d" % (deleted_fold)
	print "Total not deleted: %d" % (nodeleted)
	print "Total check: %d/%d" % (deleted_fold+nodeleted,len(OBList)*len(bandList))

	return 0
				
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
