#!/usr/bin/python

import sys
import re

def usageInfo():
    print ">>>>>"
    print "This script adds entry log to every function in the file."
    print "Usage: "+sys.argv[0]+" <path>/<file>"
    print "Output: <path>/<file>_changed"
    print "Look for log: _swat_ <file> <function>"
    print "Note: Compare original and changed file before use."
    print "<<<<<"
    return

try:
    inFile = sys.argv[1]
    f = open(inFile, "r")
except:
    print "ERR: invalid use"
    usageInfo()
    quit()

print ">>>>>"
print "Processing file: " + inFile + "\n"
contents = f.readlines()
f.close()
matchCount = 0

userPattern = "_swat_"
functionPattern = '[^/|\*]*function '
endPattern = '(.*).*{'
stripPattern = '\(.*\).*\{'
linePattern = "^"+str(functionPattern)+str(endPattern)+"$"
pattern = re.compile(linePattern)

with open(sys.argv[1], 'r') as file:
    for lineCount, line in enumerate(file):
	match = re.search(pattern, line)
	if match:
	    matchCount = matchCount+1
	    funcStr = re.sub(stripPattern, '', re.sub(functionPattern, '', match.group()))
            print "Entry log added to function: " + str(matchCount) + ": "+ funcStr
            logStr = "debug.log('"+userPattern+" "+file.name+": "+str(matchCount)+": "+funcStr+"');\n"
	    contents.insert((lineCount+matchCount), logStr)

if matchCount:
    outFile = inFile+"_changed"
    f = open(outFile, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    print "\n" + inFile + " processed successfully"
    print "Output file is " + outFile
    print "\nTo compare files before use run:"
    print "diff " + outFile + " " + inFile
    print "\nTo use changed file run:"
    print "mv " + outFile + " " + inFile + "\n"
print "<<<<<"
