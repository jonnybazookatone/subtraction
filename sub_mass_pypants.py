#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_mass_pypants.py |
 ==============

Summary:
        Run HOTPANTS with several different PSF and STAMP sizes
Usage:
        sub_mass_pypants.py -d directory -a True/False -v True/False -b r
        
        d = directory with OB*/
        a = all or single PSF/STAMP combination
        v = verbose
        b = band

"""

from python.imclass.image import imFits
from python.subtraction.sub_pypants import main as pypants
import python.subtraction.wcsremap as remap
import os, re, glob, sys, getopt, numpy

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def parameters(verbose=False):

	# Number of subdivisions of the image
	nsxList = numpy.arange(5,20,5)
	nsyList = numpy.arange(5,20,5)
	nsxnsyList = zip(nsxList,nsyList)

	# Different types of PSF
	## 3 PSF
	psfa = [3, 6, 0.6, 4, 1.5, 2, 3]
	psfb = [3, 6, 0.8, 4, 2.0, 2, 4]
	psfc = [3, 6, 0.4, 4, 1.0, 2, 2]

	## 4 PSF NARROW
	psfd = [4, 6, 0.3, 6, 0.6, 4, 1.5, 2, 3]
	psfe = [4, 6, 0.4, 6, 0.8, 4, 2.0, 2, 4]
	#psff = [4, 6, 0.4, 6, 0.2, 4, 1.0, 2, 2]
	
	## 4 PSF WIDE
	psfg = [4, 6, 0.6, 4, 1.5, 2, 3, 2, 6]
	psfh = [4, 6, 0.8, 4, 2.0, 2, 4, 2, 8]
	psfi = [4, 6, 0.4, 4, 1.0, 2, 2, 2, 4]

	## 5 PSF
	psfj = [5, 6, 0.3, 6, 0.6, 4, 1.5, 2, 3, 2, 6]
	psfk = [5, 6, 0.4, 6, 0.8, 4, 2.0, 2, 4, 2, 8]
	#psfl = [5, 6, 0.4, 6, 0.2, 4, 1.0, 2, 2, 2, 4]

	#psfList = [psfa, psfb, psfc, psfd, psfe, psff, psfh, psfi, psfj, psfk, psfl]
	psfList = [psfa, psfb, psfc, psfd, psfe, psfh, psfi, psfj, psfk]

	gridcube = []
	counter = 0
	for i in range(len(nsxnsyList)):

		nsx, nsy = nsxnsyList[i]
		
		for j in range(len(psfList)):
			tempcube = []

			psf = psfList[j]
			tempcube.append(counter)
			tempcube.append(nsx)
			tempcube.append(nsy)
			for k in range(len(psf)):
				psfpar = psf[k]
				tempcube.append(psfpar)

			gridcube.append(tempcube)
			counter = counter + 1

	if verbose:
		print "Parameter grid cube created:"
		for grid in gridcube:
			print "%s" % grid				
	return gridcube	

def big_pants(directory, allpars=False, verbose=False, band=False):

	print "#########################"
	print "MASS HOTPANTS SUBTRACTION"
	print "#########################"


	# Make folder list
	print "Given directory: %s" % directory
        OBList = glob.glob("%s/OB*" % directory)
	Missing_list = []
	Skipped_list = []
	if not band:
		bandList = ["g", "r", "i", "z", "J", "H", "K"]
	else:
		bandList = [band]

	
	# Run over OBs
	for OB in OBList:
		print "#####################"
		for band in bandList:

			if allpars:
				gridcube = parameters(verbose=False)
			else:
				print "Using default input grid parameter."
				gridcube = [0, 20, 20, 3, 6, 0.59999999999999998, 4, 1.5, 2, 3]

			for cube in gridcube:

				print "OB: %s" % (OB)
				print "band: %s" % (band)
				print "cube id: %d" % (cube[0])
				print "cube input: %s" % (cube[1:])
	
				bandpath = "%s/%s" % (OB,band)

				templatefile = "%s/template_cut_%s.fits" % (bandpath, band)
				inputfile = "%s/remcut_%s.fits" % (bandpath, band)
				subpath = "%s/sub" % (bandpath)
				cubeoutpath = "%s/cube_%s" % (subpath,cube[0])
				outfile = "%s/diff_%s.fits" % (cubeoutpath, band)

				flag = False
				try:
					os.mkdir(subpath)
					print "Master subtraction folder made: %s" % (subpath)
				except:
					print "Master subtraction folder already exists"
				try:
					os.mkdir(cubeoutpath)
					print "Cube folder sucessfully made."
				except:
					print "Cube folder already exists."

				#if not os.path.exists(templatefile):
				#	print "Template in band: %s, does not exist, skipping." % band
				#	flag = True
				#	Missing_list.append([OB, band])
				if not os.path.exists(bandpath):
					print "This band has no folder, skipping."
					Missing_list.append([OB, band])
					flag = True
				if not os.path.exists(inputfile):
					print "This has no input fits image, skipping."
	                                Missing_list.append([OB, band])
					flag = True
				if os.path.exists(outfile):
					print "There is already an output file, skipping (delete it if you wish to be done again)"
					Skipped_list.append([OB, band])
					flag = True

				if not flag:
		
					imTemplate = imFits()
					imTemplate._Name = templatefile
					imTemplate._Band = band
				
					imSource = imFits()
					imSource._Name = inputfile
					imSource._Band = band

					try:
						imSubtraction = pypants(imTemplate._Name, imSource._Name, outfile, band=imSource._Band, cube=cube)
						if not os.path.exists(outfile):
							print "Hotpants failed"
						else:
							print "Hotpants worked"
					except:
						print "Hotpants failed"
			
	                                cubelog = "%s/cube.log" % (cubeoutpath)
	                                cubefile = open(cubelog, "w")
        	                        cubefile.write("%s" % (cube))
                	                cubefile.close()	

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

	# Key list for input & other constants, stupid final colon
        key_list = 'd:v:a:b:'

        # Check input
        try:
                x=sys.argv[1:]
        except:
                print __doc__ 
                sys.exit(0)

        # Take the input & sort it out
	band, directory, allpars, verbose = False, False, True, True
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')
                
		if flag == "d":
			directory = arg  
		elif flag == "v":
			if arg == "False":
				verbose = False
			else:
				verbose = True
		elif flag == "a":
			if arg == "False":
				allpars = False
			else:
				allpars = True
				
		elif flag == "b":
			band = arg
		else:
			print __doc__
			sys.exit(0)

	if directory:
		copyFits = big_pants(directory, allpars=allpars, verbose=verbose, band=band)
	else:
		print __doc__
		sys.exit(0)
