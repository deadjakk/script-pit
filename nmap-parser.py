#!/usr/bin/python
import sys
import re
if len(sys.argv) != 3:
	print ("[-]Usage: "+sys.argv[0]+" <file.nmap> <string to search for>")
	sys.exit(1)
host = ""
port = ""
with open(sys.argv[1],'r') as fh:
	for line in fh.readlines():
		line = line.strip()
		if "Nmap scan report" in line:
			host = line.split("for ")[1]
		if "open" in line:
			if sys.argv[2] in line:
				print "[PORT]Host:",host,"Port:",line
			m = re.search("[\d]{1,5}",line)
			if m:
				port = m.group(0).split("/")[0]
		if "|" in line and sys.argv[2] in line:
			print "[INFO]Host:",host,"Port:",port,"---",line
