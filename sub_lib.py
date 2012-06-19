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

def main():
	print parseIni("test.ini")

if __name__ == "__main__":
	main()
# Mon Jun 18 17:26:40 BST 2012
