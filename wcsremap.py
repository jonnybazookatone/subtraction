#Author: J Elliott
# Date: 07.11.2011
#-------------------

# imports
import sys, getopt
from python.imclass.image import imFits

# Usage

Usage = """Python wrapper for wcsremap. Relocates images to have the same pixel-pixel co-ordinates in an image using wcs
Can be used as:
	python wcsremap.py -t temp.fits -s source.fits -o out.fits -w wcsregister True/False
or imported as:
	from wcsremap import main as remap
"""

def main(templatename, sourcename, outname, wcsregister=False):

        print "WCSREMAP Python Wrapper"
        print "-----------------------"
        print ""
        
	imTemplate = imFits()
        imSource = imFits()

        imTemplate._Name = templatename
        imSource._Name = sourcename
	
	print "### WARNING ###"
	print "PYREMAP IS CHANGING THE TEMPLATE IMAGE TO MATCH THE WCS CO-ORDINATES OF THE SCIENCE IMAGE"
	print "i.e. IT IS NOT CHANGING THE SCIENCE IMAGE"
	print "###         ###"

        imOut = imTemplate.reMap(remapFits=imSource, outname=outname, wcsregister=wcsregister)

	return imOut
	

if __name__ == "__main__":

	# Key list for input & other constants, stupid final colon
        key_list = 't:s:o:w:'

        # Check input
        try:
                x=sys.argv[1]
        except:
                print Usage
                sys.exit(0)

        # Take the input & sort it out
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

		elif flag == "w":
			if arg == "False":
				wcsregister = False
			else:
				wcsregister = True
		else:
			print "Wrong input: (%s,%s)" % (opt,arg)
			print Usage
			sys.exit(0)

	main(templatename, sourcename, outname, wcsregister)	
