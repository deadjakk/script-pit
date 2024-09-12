#!/usr/bin/env python
import sys
import re

csv = False
host = ""
port = ""
outputset = set()

def add_output(hostline,port,line,term):
    ip = hostline
    host = ""

    # cleaning up the lines
    if line.startswith("#"): # removes the Nmap header
        return
    line = line.replace("  "," ")
    line = line.replace("  "," ")
    if term == "open" and csv: # helpful for dumpoing a list of all open services from a given nmap file
        line = line.replace(f" {term} ", '","')

    # adding lines to the set
    if " " in hostline:
        shost = hostline.split(" ")
        host = shost[0].replace("(","").replace(")","")
        ip = shost[1].replace("(","").replace(")","")
    if csv:
        outputset.add(f'"{host}","{ip}","{port}","{line}"')
    else:
        outputset.add(f"""[INFO]Host: {hostline} Port: {port} --- {line}""")

if len(sys.argv) < 3:
    print ("[-]Usage: "+sys.argv[0]+" <file.nmap> <string to search for> <optional: format: csv or text>")
    sys.exit(1)

if len(sys.argv) == 4:
    if 'csv' in sys.argv[3].lower():
        csv = True

if sys.argv[1].endswith(".gnmap"):
    with open(sys.argv[1],'r') as fh:
        for line in fh.readlines():
            line = line.strip()
            if line.startswith("# Nmap"):
                continue
            line = line.replace(" ","\t")
            sline = line.split("\t")
            ip = sline[1]
            host = sline[2].replace("(","").replace(")","")
            # the end, no ports here, let's not even print it (maybe later)
            if sline[3] != "Ports:":
                continue
            for pport in sline[3:]:
                if pport.endswith("///") is False and pport.endswith("///,") is False:
                    # it's not a port so we do not care
                    continue
                spport = pport.split("/")
                port_num = spport[0]
                proto    = spport[2]
                service  = spport[4]
                outputset.add(f'"{host}","{ip}","{port_num}","{service}"')

if sys.argv[1].endswith(".nmap"):
    with open(sys.argv[1],'r') as fh:
        for line in fh.readlines():
            line = line.strip()
            if "Nmap scan report" in line:
                host = line.split("for ")[1]
            if "open" in line:
                if sys.argv[2] in line:
                    add_output(host,port,line, sys.argv[2])
                m = re.search("[\d]{1,5}",line)
                if m:
                    port = m.group(0).split("/")[0]
            if "|" in line and sys.argv[2] in line:
                add_output(host,port,line, sys.argv[2])

for n in outputset:
    print(n)

