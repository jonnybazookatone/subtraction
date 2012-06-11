#!/usr/bin/python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_pypants.py |
 ==============

Summary:
        Python wrapper for hotpants. Subtraction of template image from input image, i.e. input-template.

Usage:       
        sub_pypants.py -t templatefits -s sourcefits -o outname -b band
"""

import sys, getopt
from python.imclass.image import imFits

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(templatename, sourcename, outname, band="None", cube="None"):

	print "##################################"
        print "HOTPANTS SINGLE RUN PYTHON WRAPPER"
        print "##################################"
        print ""
        
	if band == "None":
		print "Please specify band"
		sys.exit(0)

	imTemplate = imFits()
	imTemplate._Name = templatename
	imTemplate._Band = band

        imSource = imFits()
	imSource._Name = sourcename
	imSource._Band = band

#(self, templateFits, outname, _tu="None", _tuk="None", _tl="None", _tg="None", _iu="None", _iuk="None", _il="None", _ig="None", _ir="None", _nsx="None", _nsy="None", _ng="None", band="r", verbose=False)

	if cube == "None":
		_nsx = "None"
		_nsy = "None"
		_ng = "None"
	else:
		_nsx = cube[1]
		_nsy = cube[2]
		_ng = cube[3:]
	print cube

	imOut = imSource.subtractTemplate(imTemplate, outname, band=band, _nsx=_nsx, _nsy=_nsy, _ng=_ng)

	return imOut
	

if __name__ == "__main__":

	# Key list for input & other constants, stupid final colon
        key_list = 't:s:o:b:'

        # Check input
        try:
                x=sys.argv[1]
        except:
                print __doc__
                sys.exit(0)

        # Take the input & sort it out
	bandList = ["g", "r", "i", "z", "J", "H", "K"]
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')
                
			# Template
                if flag == "t":
			templatename = arg
			
			# Source
		elif flag == "s":
			sourcename = arg
		  
			# Output
		elif flag == "o":
			outname = arg  

		elif flag == "b":
			band = arg
			if band not in bandList:
				print "Band given incorrect, please use one of the following:"
				print bandList
		else:
			print "Wrong input: (%s,%s)" % (opt,arg)
			print __doc__
			sys.exit(0)

	main(templatename, sourcename, outname, band)	
