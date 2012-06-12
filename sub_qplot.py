#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_qplot.py |
 ==============

Summary:
        Quick matlotlib representation of the output magnitudes given by sub_apphot.py and sub_mass_apphot.py.

Usage:       
        sub_qplot.py --f file --t time
        f: file with magnitudes given from sub_mass_apphot
	t: time array (MJD)

        if you include a "MJD.txt" it is used to normalise the light curve to GRB t0
"""

import sys
import os
import matplotlib
import numpy
matplotlib.use("WX")
import matplotlib.pyplot as plt
from optparse import OptionParser

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def plot(infile, timefile):
	"""
	Plotting routine used. 
	It is run for a single file, so can be called multiple times.
	File input format:
	
		OBName Time Mag MagErr
	"""

	# Load time if there
	try:
		ft0 = open(timefile, "r")
		t0 = float(ft0.readlines()[0].replace("\n", ""))
		ft0.close()
		print "t0 file found, using: %f" % (t0)
	except:
		t0 = 0.0
		print "No t0 file found, using default: %f" % (t0)

	# Load and parse
	infile = open(infile, "r")
	inline = infile.readlines()
	infile.close()

	timeArray = []
	timeErrArray = []
	magArray = []
	magErrArray = []
	for i in inline:
		lsplit = i.replace("\n", "").split(" ")

		timeArray.append(float(lsplit[1]) - t0)
		timeErrArray.append(float(lsplit[2]))
		magArray.append(float(lsplit[3]))
		
		magErrArray.append(0.1)

	# seconds
	timeArray = numpy.array(timeArray) * 60*60*24.
	timeErrArray = numpy.array(timeErrArray)

	# Plot onto graph
	fig = plt.figure(0)
	ax = fig.add_subplot(111)
	ax.errorbar(timeArray, xerr=numpy.array(timeErrArray), y=magArray, yerr=magErrArray, fmt="o")
	ax.invert_yaxis()
	ax.set_xlabel("Time [s]")
	ax.set_ylabel("Brightness [mag]")
	ax.set_xscale("log")
	plt.draw()

if __name__ == "__main__":

        parser = OptionParser()
        parser.add_option('--f', dest='filelist', help='input aperture file', default=None)
        parser.add_option('--t', dest='time', help='time of grb t0', default=None)
        (options, args) = parser.parse_args()

	if options.filelist and options.time:
		plot(options.filelist, options.time)
		plt.show()
	else:
		print __doc__
# Wed Apr 11 17:06:06 CEST 2012
