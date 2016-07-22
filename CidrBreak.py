#!/usr/bin/python
#Author: Phil Grimes @grap3_ap3	
#Python 2.7.3 (default, Jul 24 2012, 11:41:34) 
#[GCC 4.7.0 20120507 (Red Hat 4.7.0-5)] on linux2
#Date: Sun 18 Nov 2012 03:20:13 PM EST 
#Revision: 1
#Description: 	cidrbreak.py is a simple subnet calculator. Give the starting subnet(s) then get text file(s) with the addresses converted.
#

import argparse, os, sys
from netaddr import IPNetwork

parser = argparse.ArgumentParser(description="Break out individual IP addresses from CIDR notation")
parser.add_argument("myFile", default='subnets.txt', help="File containing list of subnets")	#	-f == input file
parser.add_argument("-s", dest="numOfSets", help="How many sets to break into", default=1)		#	-s == # of sets to output
args = parser.parse_args()

# Global variables defined here
parsedSubnetList = []
cleanSubnetList = []
numOfSets = args.numOfSets

# Do some error checking for argv values
if len(sys.argv) < 2:
	print 'Please see help (cidrbreak.py -h) for options and try again!'

inFile = open(args.myFile, 'r')
cidrList = inFile.readlines()
inFile.close()

# Define some functions
def cleanGivenList(cidrList):	# This function strips any ugly chars from the provided subnets (Currently only \n)
	for subnet in cidrList:
		subnet = subnet.rstrip('\n')
		cleanSubnetList.append(subnet)
	return cleanSubnetList

def parseCleanList(cleanSubnetList):	# This function parses the list
	for subnet in cleanSubnetList:
		print subnet
		for host in IPNetwork(subnet):
			parsedSubnetList.append(host)
	return parsedSubnetList

def cidrBreak(cidrList,cleanSubnetList, numOfSets ):
	# Define the variables we'll be working with
	setCounter = 1
	
	# Run functions to populate our lists for working
	cleanSubnetList = cleanGivenList(cidrList)
	parsedSubnetList = parseCleanList(cleanSubnetList)
	
	# Create a parsingCounter to divide into correct number of "sets"
	parsingCounter = (len(parsedSubnetList)/int(args.numOfSets))

	# This line creates a list of lists based off of splitting the given networks divided by the specified # of sets.
	newList = [parsedSubnetList[i:i+parsingCounter] for i in xrange(0,len(parsedSubnetList), parsingCounter)]
	
	for subList in newList:
		setCounter = str(setCounter)
		file = open('set' + setCounter + '.txt', 'w')
		for each in subList:
			file.write("%s\n" % each)
		file.close()
		setCounter = int(setCounter) + 1
		
if __name__ == '__main__':
	cidrBreak(cidrList, cleanSubnetList, numOfSets )