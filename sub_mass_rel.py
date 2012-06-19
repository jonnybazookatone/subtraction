#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v2.0                   |
 ================================
| sub_mass_rel.py |
 ================
 
 Usage:
	sub_mass_rel.py --ini
	
	ini: initialisation file with the correct information inside, see the manual pages
 Summary:
	Relative photometry of the output from sub_apphot.py"""

import shutil
import glob
import logging
import optparse
import numpy
import scipy
import sys

import sub_lib
import python.lib.resultFile as resultFile

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares, Vladimir Sudilovsky"
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

logfmt = '%(levelname)s [%(asctime)s]:\t  %(message)s'
datefmt= '%m/%d/%Y %I:%M:%S %p'
formatter = logging.Formatter(fmt=logfmt,datefmt=datefmt)
logger = logging.getLogger('__main__')
#logging.root.setLevel(logging.ERROR)
logging.root.setLevel(logging.DEBUG)
#fh = logging.FileHandler(filename='%s/logs/%s.log' % (FIBYPATH, "lib")) #file handler
#fh.setFormatter(formatter)
#logger.addHandler(fh)
logging.basicConfig(format=logfmt)

def sub_mass_rel(inifile):
  
	"""Simple script to do relative photometry
	
	1. Copy all the .result files from the input folders
	2. Obtain the stars for relative photometry
	"""
	logger.info("--------------------------------------------")
	logger.info("Parsing ini file: %s" % inifile)
	sub_ini = sub_lib.parseIni(inifile)

	logger.info("--------------------------------------------")
	logger.info("Parsing relative stars")
	logger.info("--------------------------------------------")
	GRBDict, StarArray = sub_lib.parseRel(sub_ini["PHOTOMETRY"]["relstar"])
	logger.info("Object (ra,dec): %s %s" % (GRBDict["RA"], GRBDict["DEC"]))
	logger.info("Relative stars:")
	j = 1
	logger.info("\t # RA\t\tDec.\tMag\tErr")
	for i in StarArray:
		i["ID"] = j

		logger.info("\t %d %s %s %s %s" % (j, i["RA"], i["DEC"], i["MAG_ABSOLUTE"], i["MAG_ABSOLUTE_ERR"]))
		j+=1


	logger.info("--------------------------------------------")
	logger.info("Copying result files from standard reduction")
	logger.info("--------------------------------------------")

	# Obtain the OB list
	OBList = glob.glob("%s/remappings/OB*" % sub_ini["ADMIN"]["subtractiondir"])
	OBList = [i.replace("%s/remappings/" % sub_ini["ADMIN"]["subtractiondir"], "") for i in OBList]
	logger.info("OBList: %s" % OBList)

	# Copy all the .result files to the correct OB location
	calibArray = []
	for OB in OBList:
	
		search = "%s/%s/%s/*.result" % (sub_ini["ADMIN"]["observationdir"], OB, sub_ini["ADMIN"]["band"])
		resultfile = glob.glob(search)
		if len(resultfile)==1:
			resultfile = resultfile[0]
			copyfile = "%s/remappings/%s/%s/sub/best/grond.result" % (sub_ini["ADMIN"]["subtractiondir"],OB,sub_ini["ADMIN"]["band"])
			
			logger.info("Copying: %s" % resultfile)
			logger.info("Destination: %s" % copyfile)
			shutil.copy(resultfile, copyfile)
			#logger.info("Copying:\n\t%s\n\tto%s" % (resultfile, copyfile))
		elif len(resultfile)>1:
			logger.warning("Skipped: Too many result files")
			continue
		else:
			logger.warning("Skipped: No result file for: %s" % (search))
			continue
		logger.info("")

		logger.info("--------------------------------------------")
		logger.info("Relative calibration")
		logger.info("--------------------------------------------")
		logger.info("Loading .result files")
		resultDict = resultFile.resultFile("%s" % copyfile)
					
		logger.info("Aquiring reference stars from .result")
		MedianRelativeDifference = []
		OBMags = []
		for star in StarArray:
			objID = resultDict.getNearbyObjs(star["RA"], star["DEC"]).keys()[0]
			answer = sub_lib.checkdist(resultDict.objects[objID])
			print answer
			if answer < 0:
				  if answer == -1:
					  logger.info("\t #%d")
					  logger.warning("\t#%d Distance too large" % (star["ID"]))
				  elif answer == -2:
					  logger.warning("\t#%d Check failed" % (star["ID"]))
				  else:
					  logger.warning("\t#%d Unkown error" % (star["ID"]))
			else:
				  logger.info("\t#%d Found star" % (star["ID"]))
				  
			if sub_ini["ADMIN"]["band"] in ["J", "H", "K"]:
				OBMag = resultDict.objects[objID]["MAG_CALIB"] # 2MASS
				RelativeDifference = OBMag - star["MAG_ABSOLUTE"]
				
			else:
				OBMag = resultDict.objects[objID]["MAG_PSF"] # GROND ZP
				RelativeDifference = OBMag - star["MAG_ABSOLUTE"]
			logger.info("\tAbs Mag Offset")
			logger.info("\t%f %f %f" % (star["MAG_ABSOLUTE"], OBMag, RelativeDifference))
			
			MedianRelativeDifference.append(RelativeDifference)
		
		MedianRelativeError = numpy.std(MedianRelativeDifference)
		MedianRelativeDifference = numpy.median(MedianRelativeDifference)
		
		logger.info("Median Relative Difference: %f +/- %f" % (MedianRelativeDifference, MedianRelativeError))
		
		calibDict = {}
		calibDict[OB] = {}
		calibDict[OB]["MAG_REL_DIFF"] = MedianRelativeDifference
		calibDict[OB]["MAG_REL_DIFF_ERR"] = MedianRelativeError
	
	logger.info("--------------------------------------------")
	logger.info("Writing output")
	logger.info("--------------------------------------------")
	difffile = "%s/remappings/%s_diff.dat" % (sub_ini["ADMIN"]["subtractiondir"], sub_ini["ADMIN"]["band"])
	logger.info("To file: %s" % difffile)
	diffout = open(difffile, "w")
	for OB in calibDict:
		
		diffout.write("./%s %f %f" % (OB, calibDict[OB]["MAG_REL_DIFF"],calibDict[OB]["MAG_REL_DIFF_ERR"]))
	diffout.close()
	
	logger.info("--------------------------------------------")
	logger.info("Creating Absolute+Relative calibration")
	logger.info("--------------------------------------------")
	
	apphotfile = "%s/%s" % (sub_ini["ADMIN"]["subtractiondir"], sub_ini["PHOTOMETRY"]["appout"])
	logger.info("Opening sub_apphot output: %s" % (apphotfile))
	
	appout = sub_lib.parseApp(apphotfile)
	appDict = {}
	appDict["OB"] = appout[0]
	appDict["TIME"] = (appout[1])
	appDict["TIME_ERR"] = (appout[2])
	appDict["MAG"] = (appout[3])
	appDict["MAG_ERR"] = (appout[4])
	
	logger.info("Calculating relative photometry of each OB")
	logger.info("------------------------------------------")
	logger.info("\tOB Mag MagErr Diff DiffErr RelMag RelMagErr")
	
	AbsCalib = {}
	AbsCalib["OB"] = []
	AbsCalib["MAG"] = []
	AbsCalib["MAG_ERR"] = []
	AbsCalib["TIME"] = []
	AbsCalib["TIME_ERR"] = []
	
	for i in range(len(appDict["OB"])):
	 
		try:
			tempCalib = calibDict[appDict["OB"][i].replace("./", "")]
					
			mag = tempCalib["MAG_REL_DIFF"] + appDict["MAG"][i]
			mag_err = scipy.sqrt(tempCalib["MAG_REL_DIFF_ERR"]**2 + appDict["MAG_ERR"][i]**2)
			
			AbsCalib["OB"].append(appDict["OB"][i])
			AbsCalib["MAG"].append(mag)
			AbsCalib["MAG_ERR"].append(mag_err)
			AbsCalib["TIME"].append(appDict["TIME"][i])
			AbsCalib["TIME_ERR"].append(appDict["TIME_ERR"][i])
		except:
			logger.warning("No OB match for: %s"  % appDict["OB"][i])
			mag=0
			mag_err=0
			logger.warning("%s" % sys.exc_info())
			
		logger.info("\t%s %.2f %.2f %.2f %.2f %.2f %.2f" % (appDict["OB"][i], appDict["MAG"][i], appDict["MAG_ERR"][i], tempCalib["MAG_REL_DIFF"], tempCalib["MAG_REL_DIFF_ERR"], mag, mag_err))
		
	relabf = open(sub_ini["PHOTOMETRY"]["relout"], "w")
	logger.info("Writing to absolute+relative photometry to file: %s" % (sub_ini["PHOTOMETRY"]["relout"]))
	for i in range(len(AbsCalib["OB"])):
		relabf.write("%s %f %f %f %f\n" % (AbsCalib["OB"][i], AbsCalib["TIME"][i], AbsCalib["TIME_ERR"][i], AbsCalib["MAG"][i], AbsCalib["MAG_ERR"][i]))
	relabf.close()
	
	logger.info("Finished")
	

if __name__ == "__main__":

	parser = optparse.OptionParser()
        parser.add_option('--ini', dest='ini', help='ini file', default=None)
        (options, args) = parser.parse_args()
        
        
        if options.ini:
		sub_mass_rel(options.ini)
	else:
		print __doc__
# Tue Jun 19 09:57:43 BST 2012
