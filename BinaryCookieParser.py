##!C:\Python27\python.exe
## Author: Tomas FEARON
## Script: BinaryCookieParser.py
## Purpose: Parses URLs and Google Analytics time stamps from binary cookie files and outputs to a CSV

## Import modules
import re, time, sys

## Define Usage
if len(sys.argv)!=2:
	print "\nUsage: Python BinaryCookieParser.py [Full path to Cookies.binarycookies file] \n"
	print "Example: Python BinaryCookieParser.py C:\Cookies.binarycookies"
	sys.exit(0)

FilePath = sys.argv[1]
	
## Read cookie data from supplied file path
try:
    opencookie=open(FilePath, 'rb')
except IOError as e:
    print 'File Not Found: '+ FilePath
    sys.exit(0)
	
## Read content and close
cookiecontent = opencookie.readlines()
opencookie.close()

##  Create list for results
results = []

## Define regex
regex = re.compile(b'(A\.(\w+\.(\w+|\w+\.\w+))\x00_ga\x00/\x00GA\d\.\d\.\d+\.(\d{10}))')


##Search for matches

print 'Now Searching...'

i = 0

while i !=len(cookiecontent):
	
	matches = re.findall(regex, cookiecontent[i])
	
	# Parse URL and timestamp. Convert UNIX timestamp to ISO time
	for match in matches:
		url = match[1]
		ts = match[3]
		intts = int(ts)
		ts = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(intts))
		results.append("%s,%s" % (url,str(ts)))
	i += 1
	
## sort results alphabetically
results = sorted(results)	

## Get current timestamp
nowts = time.time()
nowts = time.strftime("%Y-%m-%d %H%M%S",time.gmtime(nowts))

## Get file name for output CSV
OutputName = '%s - ' % (nowts) + raw_input('Parsing Complete. What would you like to call your output csv?: ')

## Create output file as write
output = open('%s.csv' % (OutputName) , 'w')

# Write data to output file
output.write('Binary File Parser Output\n')
output.write('%s,%s' % ('URL','Timestamp of first time cookie set for user (UTC)\n'))
for item in results:
	output.write(str(item) + '\n')
