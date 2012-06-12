#!/usr/bin/env python
"""
 ================================
| HOTPANTS Data Analysis Pipeline |
|         v1.0                   |
 ================================
| sub_relative_phot.py |
 ==============

Summary:
        Hack for relative photometry utilising the output from gr_lc2.py.

Usage:       
        sub_relative_phot.py -r '*_rel.rxr' -s 'band_appmag.dat' -b 'band'
"""

import getopt, sys, numpy
import matplotlib.pyplot as plt

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2012"
__credits__ =  "Felipe Olivares"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(thomasfile, subfile, TIMEZP, band):

	# Script outline
	# 
	# 1. Open and parse the data from the gr_lc2.py output
	# 2. Open and parse the data from the sub script
	# 3. Do relative photometry by matching MJD times


	# 1. gr_lc2.py, read
	rel_photfile = open(thomasfile, "r")
	rel_phot = rel_photfile.readlines()
	rel_photfile.close()

	## parse
	relative = []
	for phot in rel_phot:
		if phot[0] != "#":
			photline = [i for i in phot.replace("\n","").replace("\t"," ").split(" ") if i != ""]
			relative.append(photline)

	# 2. subtraction magnitudes
	sub_photfile = open(subfile, "r")
	sub_phot = sub_photfile.readlines()
	sub_photfile.close()

	## parse
	subtraction = []
	for sphot in sub_phot:
		subline = [i for i in sphot.replace("\n", "").split(" ") if i != ""]
		subtraction.append(subline)

	
	# match
	match = numpy.zeros( (len(subtraction), 4) )
	i, j = 0, 0
	for SUB in subtraction:
		for PHOT in relative:
			SUBTIME = float(SUB[1])
			PHOTTIME = float(PHOT[0])

			DIFF = abs(SUBTIME-PHOTTIME)*60*60*24
			if DIFF < 10:
				#print "%f" % DIFF
				if SUB[2] != "INDEF" and SUB[3] != "INDEF":
					print SUB
					mag = float(SUB[2])
					magerr = float(SUB[3])
					time = (float(PHOT[0]) - float(TIMEZP))*60*60*24
					timeerr = float(PHOT[1])
				
					zpdiff = float(PHOT[4])

					match[i][0] = time
					match[i][1] = timeerr
					match[i][2] = mag+zpdiff
					match[i][3] = magerr
		
					i += 1
				else:
					print "Photometry missing"
					print SUB
	#Check
#	print "Length of subtracted: %f" % (len(subtraction))
#	print "Length of relative: %f" % (len(relative))
#	print "Length of match: %f" % (len(match))


#	fig = plt.figure(0)
#	ax = fig.add_subplot(111)
#	ax.plot(match[:,0:1], -1*match[:,2:3], 'o')
#	ax.set_xscale('log')

#	plt.show()

	# Write to file to use with LC_model.py
        filename = open("%s_AB.txt" % band, "w")
	for i in range(len(match)):
		if match[i][2] != 0:
			filename.write("%f %f %f %f\n" % (match[i][0], match[i][1], match[i][2], match[i][3]))
	filename.close()

if __name__ == "__main__":

	timezp = 55822.89371528 

        key_list = "r:s:b:"
        rel, sub, band = None, None, None

        # Obtain input
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')

                if flag == "r":
                        rel = arg
                elif flag == "s":
                        sub = arg
		elif flag == "b":
			band = arg
#               elif flag == "x":
#                       ra = arg
#               elif flag == "y":
#                       dec = arg
                else:
                        print __doc__
                        sys.exit(0)

	if sub and rel and band:
	        main(rel, sub, timezp, band)
	else:
		print sys.exc_info()[0]
                print __doc__

# Mon Dec 12 15:53:33 CET 2011
