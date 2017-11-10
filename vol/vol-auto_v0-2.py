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

# Output settings

OutputDir = datetime.now().strftime(TimeStampFormat)+'/'
OutputFile = 'vol-auto-results_'+datetime.now().strftime(TimeStampFormat)+'.db'
OutputCnfg = '--output=sqlite --output-file='+OutputDir+OutputFile

# Volatility plugins

pluginCnfg = 	[	['pslist',	'psscan',	'psxview',	'ldrmodules',	'apihooks',	'malfind',	'svcscan',	'devicetree'],
					['no',		'no',		'no',		'no',			'no',		'no',		'no',		'no']
				]

#### CODE START 

def main(argv):
	
    #### Inputs 

	VolFile = ''                # Path to vol.py
	ImageFile = ''              # Input file (mem. dump)
	InputImageProfile = ''      # Input image profile (e.g. Win10x64_15063)

	try:
		opts, args = getopt.getopt(argv,"hv:i:p:",["vfile=","ifile=","iiprofile="])
	except getopt.GetoptError:
		print 'vol-auto.py -v <path to vol.py> -i <inputfile> -p <image-profile>'
		sys.exit('Script fail')
	for opt, arg in opts:
		if opt == '-h':
			print 'vol-auto.py -v <path-to-vol.py> -i <inputfile> -p <image-profile>'
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

	print datetime.now().strftime(TimeStampFormat)+' Output DB file: '+OutputDir+OutputFile

	#### Executing functions 

	print datetime.now().strftime(TimeStampFormat),'Analysis starting...'

	cmdString = ''

	for i in range(len(pluginCnfg[0])):
		if pluginCnfg[1][i] == "yes":
			print datetime.now().strftime(TimeStampFormat),'Task start:', pluginCnfg[0][i]
			
			cmdString = 'python '+VolFile+' -f '+ImageFile+' --profile='+InputImageProfile+' '+OutputCnfg+' '+pluginCnfg[0][i]
			
			if pluginCnfg[0][i] == "malfind":
			
				try: # Checking and creating output folder
					os.makedirs(OutputDir+'malfind-output/')
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise
			
				cmdString = cmdString+' -D '+OutputDir+'malfind-output/' 
			
			subprocess.call(cmdString, shell=True) 
			
			print datetime.now().strftime(TimeStampFormat),'Task complete:', pluginCnfg[0][i]
			
	print datetime.now().strftime(TimeStampFormat),'Analysis complete!' # todo: check if functions returned without errors


#### SCRIPT COMPLETE 

if __name__ == "__main__":      # https://stackoverflow.com/questions/419163/what-does-if-name-main-do
	main(sys.argv[1:])

