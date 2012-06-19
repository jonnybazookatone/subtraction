#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v2.0                   |
 ================================
| sub_lib.py |
 ============
 
 Library for routines for v2.0 of the HOTPANTS pipeline"""

import sys

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def parseIni(filename):
  
	inifile = open(filename, "r")
	iniin = inifile.readlines()
	inifile.close()
	
	iniDict = {}
	dictname = False
	
	for ini in iniin:
		line = ini.replace("\n", "")
		
		if line[0] == "[":
			
			dictname = line.replace("[", "").replace("]", "")
			iniDict[dictname] = {}
			continue
		if not dictname:
			print "ini of wrong type"
			sys.exit(0)
			
		equalline = line.split("=")
		if equalline[1].replace(".","").isdigit():
			iniDict[dictname][equalline[0]] = float(equalline[1])
		else:
			iniDict[dictname][equalline[0]] = equalline[1]
		
	return iniDict

def parseRel(relfile):
	
	"""Parse the star file given for relative astronomy"""
	relf = open(relfile, "r")
	relfline = relf.readlines()
	relf.close()
	
	# First line is GRB
	grb = relfline[0].replace("\n","").split(" ")
	GRBDict = {}
	GRBDict["RA"] = float(grb[0])
	GRBDict["DEC"] = float(grb[0])
	
	StarArray = []
	# Other lines are magnitudes
	for i in relfline[1:]:
		  starline = i.replace("\n","").split(" ")
		  StarDict = {}
		  StarDict["RA"] = float(starline[0])
		  StarDict["DEC"] = float(starline[1])
		  StarDict["MAG_ABSOLUTE"] = float(starline[2])
		  StarDict["MAG_ABSOLUTE_ERR"] = float(starline[3])
		  
		  StarArray.append(StarDict)
		  
	return GRBDict, StarArray

def checkdist(obj):
	try:
		if obj["DISTANCE"]>2:
			return -1
		else:
			return 0
	except:
		return -2

def parseApp(infile):
	# Load and parse
	infile = open(infile, "r")
	inline = infile.readlines()
	infile.close()

	OBArray = []
	timeArray = []
	timeErrArray = []
	magArray = []
	magErrArray = []
	for i in inline:
		lsplit = i.replace("\n", "").split(" ")

		OBArray.append(lsplit[0])
		timeArray.append(float(lsplit[1]))
		timeErrArray.append(float(lsplit[2]))
		magArray.append(float(lsplit[3]))
		
		magErrArray.append(float(lsplit[4]))
	
	return OBArray, timeArray, timeErrArray, magArray, magErrArray

def main():
	print parseIni("test.ini")

if __name__ == "__main__":
	main()
# Mon Jun 18 17:26:40 BST 2012
