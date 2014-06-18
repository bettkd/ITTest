#!/usr/bin/python
#Author: Dominic Bett
#Date: 6/5/2014
#Company: Dell Inc
import os

'''Global variables'''
hostfname = 'Hosts.list'
testDirPath = '../TkinterApps'

'''Class definition'''
class ITFunctions:		

	#_________________________________________
	#Reading Host Attributes From File
	'''Reading File, Returns Array of Lines in File'''
	def readFileToArray(self, filename):
		lines = [line.rstrip('\n') for line in open(filename)]
		return lines
	
	'''Split the lines and return list of host names of ips'''
	def getHostAndIP(self, lines):
		hostnames = []
		ips = []
		for x in xrange(0, len(lines)):
			(h, i) = lines[x].split(':')
			hostnames.append(h)
			ips.append(i)
		return (hostnames, ips)
	
	'''Depending on the parameter, return a specific list'''
	'''Reads from the file'''
	def hostItem(self, hostOrIP):
		lines = self.readFileToArray(hostfname)
		if hostOrIP == 'hostnames':
			return self.getHostAndIP(lines)[0]
		elif hostOrIP == 'ips':
			return self.getHostAndIP(lines)[1]
		else:
			print 'Error: Invalid option \nChoose: [\'host\'] or [\'ips\']'
	#_________________________________________

	#_________________________________________
	#Reading Test Attributes From File
	'''Read Directory Paths and Files into Array'''
	def getDirsFiles(self):
		dirpaths = []
		filenames = []
		for root, dirs, files in os.walk(testDirPath, topdown=False):
			for name in dirs:
				dir_path = os.path.join(root, name)
				dirpaths.append(dir_path)
				filenames.append(os.listdir(dir_path))
		#print "____________\n", dirpaths
		return (dirpaths, filenames)

'''Test'''
def main():

	itf = ITFunctions()
	#print itf.hostItem("hostnames")
	#print itf.hostItem("ips")
	
	d, f = itf.getDirsFiles()
	print f

if __name__ == '__main__':
	main()