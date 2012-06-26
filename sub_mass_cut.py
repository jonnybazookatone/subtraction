#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_mass_cut.py |
 ==============

Summary:
        Make mass cuts
Usage:
        python sub_makemass_cut.py --d directory --b band --v True/False --r regionfile --OB
        
	d: directory of the remapped OB files
	b: band
	v: verbose output [Default: True]
	r: region file for cutting [Default: False]
	OB: OB list separated by commas
"""

from python.imclass.image import imFits
from python.subtraction.sub_cut import main as make_cut
import python.subtraction.wcsremap as remap
import os, re, glob, sys
from optparse import OptionParser

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

Usage = """"""

def main(directory, band=None, verbose=False, regionflag=None, OBList=False):

	print "------------------"
	print "MASS PYRAF CUTTING"
	print "------------------"

	print "Utilises region files that must exist in all folders"
	print ""

	# Make folder list
	print "Given directory: %s" % directory
	if not OBList:
		OBList = glob.glob("%s/OB*" % directory)
		print "OBList: %s" % OBList
	else:
		print "User defined OBList: %s" % OBList

	Missing_list = []
	Skipped_list = []
	if not band:
		bandList = ["g", "r", "i", "z", "J", "H", "K"]
	else:
		bandList = [band]
	

	# Check template dir exists
	#if not os.path.exists(templatedirectory):
	#	print "Template directory does not exist"
	#	sys.exit(0)

	# Run over OBs
	for OB in OBList:
		print "#####################"
		for band in bandList:
			print "OB: %s" % (OB)
			print "band: %s" % (band)
			bandpath = "%s/%s" % (OB,band)
			if regionflag:
				regionfile = regionflag
			else:
				regionfile = "%s/cut.reg" % (bandpath)
			print "regionfile: %s" % regionfile

                        infile1 = "%s/science_mapping_%s_mko.fits" % (bandpath, band)
                        infile2 = "%s/science_mapping_%s.fits" % (bandpath, band)

			if os.path.exists(infile1):
				infile = infile1
				print "science format used: %s" % infile
			elif os.path.exists(infile2):
				infile = infile2
                                print "science format used: %s" % infile
			else:
				print "Format not recognised"
				sys.exit(0)

			outfile = "%s/remcut_%s.fits" % (bandpath, band)
			templateband = "%s/template_remapping_%s.fits" % (bandpath, band)
			templateout = "%s/template_cut_%s.fits" % (bandpath, band)

			flag = False
			outflag = False
			tempflag = False

			if not os.path.exists(templateband):
				print "Template in band: %s, does not exist. We take form GROND_(band)_OB_ana.fits."
				flag = True
				Missing_list.append([OB, band])
			if not os.path.exists(bandpath):
				print "This band has no folder, skipping."
				Missing_list.append([OB, band])
				flag = True

			if not regionfile:
				if not os.path.exists(regionfile):
					print "This band has no region file, skipping."
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

			if os.path.exists(templateout):
				print "There is already an output template, skipping (delete it if you wish to be done again)"
				Skipped_list.append([OB, band])
				tempflag = True

			if not flag:
				regionfile = open(regionfile, "r")
				region = regionfile.readlines()[0].replace("\n", "")
				regionfile.close()
				print "Region used: %s" % region

				if not outflag:
					imCopy = make_cut(infile, outfile, region, verbose)
				if not tempflag:
					templateCopy = make_cut(templateband, templateout, region, verbose)

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
        parser.add_option('--d', dest='directory', help='directory of OBs', default=None)
        parser.add_option('--v', dest='verbose', help='verbose output', default=False)
        parser.add_option('--r', dest='regionfile', help='region file for cutting', default=False)
        parser.add_option('--b', dest='band', help='band', default=None)
        parser.add_option('--OB', dest='OBList', help='OB list to use', default=False)
        (options, args) = parser.parse_args()

	if options.directory and options.band:
	  
		if options.OBList:
			OBList = options.OBList.split(",")
		else:
			OBList = options.OBList
		copyFits = main(options.directory, options.band, options.verbose, options.regionfile, OBList)
	else:
		print __doc__
		sys.exit(0)
