#!/usr/bin/env python
import os,sys
import argparse

TESTDATA = """    <add key="SomeConnectionString" value="Data Source=somecomputer.com;Initial Catalog=somecatalog;Integrated Security=false;user id=someuser;password=somepassword;Application Name=someappname" />"""

def parse_section(section_name, line):
    section_start_index = line.lower().rfind(section_name)+1+len(section_name)
    try:
        sec_line = line[section_start_index:len(line)].split(";")[0]
        return sec_line
    except:
        return

def parse_line(line,file_name):
    roi = ''
    try:
        roi = line[line.rfind('value=')+len('value=')+1:len(line)-1]
    except:
        print(f'err parsing line {line}')
        return
    user = parse_section("user id", roi)
    password = parse_section("password", roi)
    source = parse_section("data source", roi)
    print(f"found in {file_name}:")
    print(f"\t{user}:'{password}'@{source}")


parser = argparse.ArgumentParser()
parser.add_argument('i', help='input file')
args = parser.parse_args()

if os.path.exists(args.i) is False:
    print('err, file {args.i} does not exist', file=sys.stderr)
    exit(1)
with open(args.i,'r') as fh:
    for line in fh.readlines():
        line=line.strip()
        if 'data source' not in line.lower() or 'password' not in line.lower():
            continue
        parse_line(line,args.i)
