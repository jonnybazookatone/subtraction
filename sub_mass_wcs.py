#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_mass_wcs.py |
 ==============

Summary:
        Remaps the images located in OB/band/* to the template pixel co-ordinates.
Usage:
        sub_mass_wcs.py --t tempalte --d dir --w True/False --b r --OB OB1_3
        
        t: template image
        d: directory of files OB/...
        w: wcsregister [True], WCSREMAP [False]
        b: band [grizJHK], all = None
        OB: an OB list separated by commas, default is all OBs
        

        output: OB/band/subtraction/remappings/input_remapping.fits
"""

import python.subtraction.wcsremap as remap
import os, re, glob, sys, getopt, shutil
from optparse import OptionParser

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(TemplateImagePath, PATH, band=None, wcsregister=True, OBList=False):

	# Logger
	logger = {}
	logger['Info'] = []

	# Bands
	if not band:
		bandList = ["g", "r", "i", "z", "J", "H", "K"]
	else:
		bandList = [band]
	print "Band list: %s" % bandList

	# This is shaping all the images I need into pixel co-ordinates

	
	#PATH = "/diska/home/jonny/reduction/GRB110918A"
	#TemplateImagePath = "%s/host/OB10_12"
	OutputPath = "%s/subtraction/remappings" % (PATH)
	
	# Output folder
	try:
		os.mkdir(OutputPath)
		logger['Info'].append("Output path created.")
	except:
		logger['Info'].append("Output path already exists.")


	# Look for all the OB folders
	if not OBList:
		OBList = glob.glob("%s/OB*/" % (PATH))
		print "OB list: %s" % OBList
	else:
		print "User defined OB list: %s" % OBList

	# Now do image reshaping and print to user
	for OBPath in OBList:

		OB = [i for i in OBPath.split('/') if i != ""]
		OB = OB[-1]
		logger[OB] = []
		logger[OB].append("Starting with OB: %s" % (OB))
		# Make the folder
		
		outFolder = "%s/%s" % (OutputPath, OB)
		try:
			os.mkdir(outFolder)
			logger[OB].append("OB folder created.")
		except:
			logger[OB].append("OB folder already exists.")
		
		for band in bandList:
			logger[OB].append("Band: %s" % (band))
			# Make the band directory
			try:
		                bandFolder = "%s/%s/%s" % (OutputPath, OB, band)
				os.mkdir(bandFolder)
				logger[OB].append("Band folder created")
			except:
				logger[OB].append("Band folder already exists")

			# Match the ana file
			anafile = glob.glob("%s/%s/%s/GROND_%s_OB_ana.fits" % (PATH, OB, band, band))
			logger[OB].append("Ana file used: %s" % (anafile))

			if len(anafile)>1:
				anafile = anafile[0]
				logger[OB].append("too many ana files, first used: %s" % anafile)
			elif len(anafile)==1:
				anafile = anafile[0]
				logger[OB].append("anafile used: %s" % anafile)
			elif len(anafile)==0:
				print "FAILURE FINDING ANA FILE"
				print "Template: %s" % template

			if anafile:
				try:
					print "Given anafile: %s" % anafile
					anafile = "%s/%s" % (os.getcwd(), anafile)
					print "Trying to copy science image: %s" % (anafile)
					anacopy = "%s/science_mapping_%s.fits" % (bandFolder, band)
					shutil.copy(anafile, anacopy)
					print "Copied science image to subtraction directory"
				except:
					print "Failed to copy science image to subtraction directory"
			else:
				print "No anafile"

			# Do image re-alignment
			template = glob.glob("%s/%s/GROND_*_OB*_ana.fits" % (TemplateImagePath, band))
			if len(template)>1:
				template = template[0]
				logger[OB].append("too many templates, first used: %s" % template)
			elif len(template)==1:
				template = template[0]
				logger[OB].append("template: %s" % template)
			elif len(template)==0:
				print "FAILURE FINDING TEMPLATE"
				print "Template: %s" % template
			output = "%s/template_remapping_%s.fits" % (bandFolder, band)
			print "Template used: %s" % (template)
			print "Template output: %s" % (output)

			print ""
			if type(output) == str and type(template) == str and type(anafile) == str:
				outImage = remap.main(template, anacopy, output, wcsregister)
			else:
				print 'OB, Band: %s, %s' % (OB, band)
				print 'ERROR: NO STRINGS FOR THIS RUN, FAILED'

		print ""
		print ""
		print "Information on run:"
		print ""	
		fop = open("logging.log", "w")
		for log in logger[OB]:
			print log
			fop.write(log+'\n')
		print ""
		print "#######################"
		fop.close()


if __name__ == "__main__":
        
        parser = OptionParser()
        parser.add_option('--d', dest='directory', help='directory of OBs', default=None)
        parser.add_option('--t', dest='template', help='template', default=None)
        parser.add_option('--w', dest='wregister', help='use wregister [Default: True]', default=None)
        parser.add_option('--b', dest='band', help='band', default=None)
        parser.add_option('--OB', dest='OBList', help='OB list to use', default=False)
        (options, args) = parser.parse_args()

	if options.template and options.directory and options.band:
	  
		if options.OBList:
			OBList = options.OBList.split(",")
		else:
			OBList = options.OBList
		main(options.template, options.directory, options.band, options.wregister, OBList)
	else:
		print __doc__
		sys.exit(0)
