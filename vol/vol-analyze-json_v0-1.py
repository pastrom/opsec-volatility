#
# Script for automating Volatility functions on a memory dump.
#
# todo:
# 
# - Hvordan fa til a fa analyselogger i en egen fil
# - Sjekk av filer og mapper
#


#### IMPORTS ##############

import sys, getopt, subprocess, os, errno
from datetime import datetime


#### CODE START ############

def main(argv):
    
    #### Inputs 

	VolFile = ''                # Path to vol.py
	ImageFile = ''              # Input file (mem. dump)
	InputImageProfile = ''      # Input image profile (e.g. Win10x64_15063)
    # OutputPath = ''           # Specify output path 
  
	try:
		opts, args = getopt.getopt(argv,"hv:i:p:",["vfile=","ifile=","iiprofile="])
	except getopt.GetoptError:
		print 'vol-analyze-json.py -v <path to vol.py> -i <inputfile> -p <image-profile>'
		sys.exit('Script fail')
	for opt, arg in opts:
		if opt == '-h':
			print 'vol-analyze-json.py -v <path-to-vol.py> -i <inputfile> -p <image-profile>'
			sys.exit('Help command.')
		elif opt in ("-v", "--vfile"):
			VolFile = arg
		elif opt in ("-i", "--ifile"):
			ImageFile = arg
		elif opt in ("-p", "--iiprofile"):
			InputImageProfile = arg
            
  
    #### Configurations

    TimeStampFormat = '%Y-%m-%d_%H-%M-%S'
    OutputDir = datetime.now().strftime(TimeStampFormat)+'/'
            

    #### Prepare execution
            
    print datetime.now().strftime(TimeStampFormat),'Using vol.py at: ', VolFile
	print datetime.now().strftime(TimeStampFormat),'Input file: ', ImageFile
	print datetime.now().strftime(TimeStampFormat),'Input image profile: ', InputImageProfile
   
    try: # Checking and creating output folder
        os.makedirs(OutputDir)
        print datetime.now().strftime(TimeStampFormat),'Output dir: ', OutputDir
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
    
	#### Executing functions 
    
	print datetime.now().strftime(TimeStampFormat),'Analysis starting...'


	# PSLIST
	print datetime.now().strftime(TimeStampFormat),'Task start: PSLIST'
	PslistCmd = 'python '+VolFile+' pslist -f '+ImageFile+' --profile='+InputImageProfile+'--output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-pslist.json'
	subprocess.call(PslistCmd, shell=True) 
	print datetime.now().strftime(TimeStampFormat),'Task complete: PSLIST'

	# PSSCAN
	print datetime.now().strftime(TimeStampFormat),'Task start: PSSCAN'
	PsscanCmd = 'python '+VolFile+' psscan -f '+ImageFile+' --profile='+InputImageProfile+'--output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-psscan.json'
	subprocess.call(PsscanCmd, shell=True) 
	print datetime.now().strftime(TimeStampFormat),'Task complete: PSSCAN'

	# LDRMODULES
	# print datetime.now().strftime(TimeStampFormat),'Task start: LDRMODULES'
	# LdrmodulesCmd = 'python '+VolFile+' ldrmodules -f '+ImageFile+' --profile='+InputImageProfile+' '+OutputConfig+'-ldrmodules.json'
	# subprocess.call(LdrmodulesCmd, shell=True) 
	# print datetime.now().strftime(TimeStampFormat),'Task complete: LDRMODULES'


    #### SCRIPT COMPLETE 

	print datetime.now().strftime(TimeStampFormat),'Analysis complete!' # todo: check if functions returned without errors
    

if __name__ == "__main__":      # https://stackoverflow.com/questions/419163/what-does-if-name-main-do
	main(sys.argv[1:])


