#!/usr/bin/python

import sys
import re

stPtrn = " >>> "
ndPtrn = " <<< "
userPattern = stPtrn + "swat" + stPtrn
lookForStr = "Look for log: "+userPattern+"file"+stPtrn+"func#"+stPtrn+"funcName"+ndPtrn
functionPattern = '[^/|\*]*function '
endPattern = '(.*).*{'
stripPattern = '\(.*\).*\{'
# ^[^/|\*]*function (.*).*{$
linePattern = "^"+str(functionPattern)+str(endPattern)+"$"

def usageInfo():
    print "This script adds entry log to every function in the file."
    print "Usage: "+sys.argv[0]+" <path>/<file>"
    print "Output: <path>/<file>_changed"
    print lookForStr
    return

try:
    inFile = sys.argv[1]
    f = open(inFile, "r")
except:
    print "ERR: invalid use"
    usageInfo()
    quit()

print "\n" + "Processing file: " + inFile + "\n"
contents = f.readlines()
f.close()
matchCount = 0
pattern = re.compile(linePattern)

with open(sys.argv[1], 'r') as file:
    for lineCount, line in enumerate(file):
	match = re.search(pattern, line)
	if match:
	    matchCount = matchCount+1
	    funcStr = re.sub(stripPattern, '', re.sub(functionPattern, '', match.group())).strip()
            print "Entry log added to function: " + str(matchCount) + ": "+ funcStr
            if funcStr:
                funcStr = stPtrn + funcStr
            logStr = "debug.log('"+userPattern+file.name+stPtrn+str(matchCount)+funcStr+ndPtrn+"');\n"
	    contents.insert((lineCount+matchCount), logStr)

if matchCount:
    outFile = inFile+"_changed"
    f = open(outFile, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    print "\n" + inFile + " processed successfully"
    print "Output file is " + outFile
    print lookForStr
    print "\nTo compare files before use run:"
    print "vimdiff " + outFile + " " + inFile
    print "\nTo use changed file run:"
    print "mv " + outFile + " " + inFile + "\n"
