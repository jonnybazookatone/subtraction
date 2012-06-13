#!/usr/bin/env python

"""Find the FWHM of the image.
Usage:
sex_fwhm.py -f \"file.fits\""""

import matplotlib.pyplot as plt
import numpy, getopt, sys

import python.lib.sextractor as sextractor

def main(filename):
	# Create a SExtractor instance
	sex = sextractor.SExtractor()

	# Modify the SExtractor configuration
	sex.config['DETECT_MINAREA'] = 8
	sex.config['DETECT_THRESH'] = 8
	#sex.config['MEMORY_BUFSIZE'] = 2048
	#sex.config['MEMORY_PIXSTACK'] = 300000
	#sex.config['ANALYSIS_THRESH'] = 4
	#sex.config['DETECT_MAXAREA'] = 10

	# Add a parameter to the parameter list
	sex.config['PARAMETERS_LIST'].append('FWHM_WORLD')
	sex.config['PARAMETERS_LIST'].append('FLAGS')

	# Lauch SExtractor on a FITS file
	sex.run(filename)

	# Print FHWM information
	catalog_name = sex.config['CATALOG_NAME']
	catalog_f = sextractor.open(catalog_name)
	catalog = catalog_f.readlines()
	FWHMList = numpy.array([])

	catalogoo = open("%s" % filename.replace(".fits","_sex_tmp.reg"), "w")

	for star in catalog:
		catalogoo.write("image; circle(%f,%f,4) # color = blue\n" % (star['X_IMAGE'], star['Y_IMAGE']))
		FWHMList = numpy.append(FWHMList,float(star['FWHM_IMAGE']))

	catalogoo.close()

        # Take the smallest 20% of the FWHM
	FWHMList = numpy.sort(FWHMList)
	FWHMListLength = len(FWHMList)
	FWHMTwenty = int(0.2*FWHMListLength)
	FWHMTwentyList = numpy.array([])

	for FWHM in range(FWHMTwenty):

		FWHMTwentyList = numpy.append(FWHMTwentyList, FWHMList[FWHM])

	medianfwhm = numpy.median(FWHMTwentyList)
    
    	# Plot
	fig = plt.figure(0)
	ax = fig.add_subplot(111)
	ax.plot(range(len(FWHMList)),FWHMList)
	ax.set_xlabel('star')
	ax.set_ylabel('FHWM/pixels')
	savename = "sex.png"
	#plt.savefig(savename, format="png")

	sex.clean(config=True, catalog=True, check=True)
	
	return medianfwhm

if __name__ == "__main__":

	        # Key list
        key_list = "f:"
	filename = None

        # Obtain input
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')

                if flag == "f":
                        filename = arg
                else:
                        print __doc__
                        print sys.exit(0)

        if filename:
                print main(filename)
        else:
                print __doc__
                sys.exit(0)
