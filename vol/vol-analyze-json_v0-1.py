#
# Script for automating Volatility functions on a memory dump.
#
# todo:
# 
# - Hvordan fa til a fa analyselogger i en egen fil
#
#


#### IMPORTS

import sys, getopt, subprocess, os, errno
from datetime import datetime


#### Configurations

TimeStampFormat = '%Y-%m-%d_%H-%M'
OutputDir = datetime.now().strftime(TimeStampFormat)+'/'

# Functions
DoPslist = 'no'
DoPsscan = 'no'
DoPsxview = "no"
DoLdrmodules = 'no'
DoApihooks = 'no'
DoMalfind = 'no'
DoSvcscan = 'no'
DoDevicetree = 'no'


#### CODE START 

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
	if DoPslist == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: PSLIST'
		PslistCmd = 'python '+VolFile+' pslist -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-pslist.json'
		subprocess.call(PslistCmd, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: PSLIST'

	# PSSCAN
	if DoPsscan == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: PSSCAN'
		PsscanCmd = 'python '+VolFile+' psscan -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-psscan.json'
		subprocess.call(PsscanCmd, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: PSSCAN'
		
	# PSXVIEW
	if DoPsxview == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: PSXVIEW'
		Psxview = 'python '+VolFile+' psxview -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-psxview.json'
		subprocess.call(Psxview, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: PSXVIEW'

	# LDRMODULES
	if DoLdrmodules == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: LDRMODULES'
		LdrmodulesCmd = 'python '+VolFile+' ldrmodules -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-ldrmodules.json'
		subprocess.call(LdrmodulesCmd, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: LDRMODULES'
		
	# APIHOOKS
	if DoApihooks == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: APIHOOKS'
		ApihooksCmd = 'python '+VolFile+' apihooks -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-apihooks.json'
		subprocess.call(ApihooksCmd, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: APIHOOKS'
	
	# SVCSCAN
	if DoSvcscan == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: SVCSCAN'
		SvcscanCmd = 'python '+VolFile+' svcscan -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-svcscan.json'
		subprocess.call(SvcscanCmd, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: SVCSCAN'
	
	# DEVICETREE
	if DoDevicetree == "yes":
		print datetime.now().strftime(TimeStampFormat),'Task start: DEVICETREE'
		DevicetreeCmd = 'python '+VolFile+' devicetree -f '+ImageFile+' --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-devicetree.json'
		subprocess.call(DevicetreeCmd, shell=True) 
		print datetime.now().strftime(TimeStampFormat),'Task complete: DEVICETREE'
	
	# malfind
	if DoMalfind == "yes":
		
		try: # Checking and creating output folder
		
			os.makedirs(OutputDir+'malfind-output/')
		
			print datetime.now().strftime(TimeStampFormat),'Task start: MALFIND'
			MalfindCmd = 'python '+VolFile+' malfind -f '+ImageFile+' -D '+OutputDir+'malfind-output/ --profile='+InputImageProfile+' --output=json --output-file='+OutputDir+datetime.now().strftime(TimeStampFormat)+'-malfind.json'
			subprocess.call(MalfindCmd, shell=True) 
			print datetime.now().strftime(TimeStampFormat),'Task complete: MALFIND'
			
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
			

	print datetime.now().strftime(TimeStampFormat),'Analysis complete!' # todo: check if functions returned without errors


#### SCRIPT COMPLETE 

if __name__ == "__main__":      # https://stackoverflow.com/questions/419163/what-does-if-name-main-do
	main(sys.argv[1:])

