#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_wcs.py |
 ==============

Summary:
        Make a wcs remap using wcsregister or wcsremap on a single image

Usage:       
        python sub_make_onewcs.py -t tempaltefits -i inputfits -o outputname -w True/False
"""

import python.subtraction.wcsremap as remap
import os, re, glob, sys, getopt

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(template, input, output, wcsregister=True):

	print "###################################"
	print "WCSREMAP/IRAF.IMCOPY PYTHON WRAPPER"
	print "###################################"

	print "Input: %s" % template
	print "Reference: %s" % input
	print "Output: %s" % output

	# Logger
	logger = {}
	logger['Info'] = []

	outImage = remap.main(template, input, output, wcsregister)

if __name__ == "__main__":

	# Key list for input & other constants, stupid final colon
        key_list = 't:i:o:w:'

        # Check input
        try:
                x=sys.argv[1]
        except:
                print __doc__ 
                sys.exit(0)

        # Take the input & sort it out
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')
                
                if flag == "t":
			templatename = arg
		elif flag == "i":
			inputname = arg  
		elif flag == "o":
			outputname = arg
		elif flag == "w":
			if arg == "True":
				wcsregister = True
			else:
				wcsregister = False
		else:
			print __doc__
			sys.exit(0)

	main(templatename, inputname, outputname, wcsregister)
