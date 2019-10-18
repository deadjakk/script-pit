#very simple mimiaktz output parser
#caution: clobbers the individual results together within each auth section
from re import match

patterns = {
	'UserName':'\t \* Username : .*\n',
	'Domain'  :'\t \* Domain   : .*\n',
	'Password':'\t \* Password : .*\n',
	'LM'      :'\t \* LM       : .*\n',
    'NTLM'    :'\t \* NTLM     : .*\n',
	'SHA1'    :'\t \* SHA1     : .*\n',
	'Domain2' :'Domain            : .*\n',
	'LoginServ':'Logon Server      : .*\n',
	'Time'    :'Logon Time        : .*\n',
	'SID'     :'SID               : .*\n',
	'msv'     :'\tmsv :\t\n',
	'tspkg'   :'\ttspkg :\t\n',
	'wdigest' :'\twdigest :\t\n',
	'kerberos':'\tkerberos :\t\n',
	'ssp'     :'\tssp :\t\n',
	'credman' :'\tcredman :\t\n'
}

states = [
	'msv',
	'tspkg',
	'wdigest',
	'kerberos',
	'ssp',
	'credman'
]

def parsemimikatzoutput(filename):
	results = []
	result = {}
	fh = False
	try:
		fh = open(filename,'r')
	except Exception as e:
		print("[-]An error ocurred opening output file:{}:{}".format(filename,e))
		return False

	for line in fh.readlines():
		if "Authentication Id" in line:
			result = {
				'UserName':'',
				'Password':'',
				'Domain':'',
				'NTLM':''
			}
		for pattern in patterns.keys():
			reResult = match(patterns[pattern],line)
			if reResult:
				if pattern in states:
					pass
				else:
					token = reResult.group().split(": ")[1].strip()
					if token and token != "(null)":
						result[pattern] = token
				if pattern == 'credman':
					if result not in results:
						results.append(result)
	return results
	
if __name__ == "__main__":
	import argparse
	import csv
	import glob
	writetofile = []
	outfile = 'parsedcreds.csv'
	perm = 'wb'
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--filename",help="file to parser, use * as a wildcard, default is parsedcreds.csv", required=True)
	parser.add_argument("-o","--outfile",help="file to save as")
	parser.add_argument("-nc","--no-clobber",help="if this is enabled, doesn't overwrite existing files", action='store_true')
	parsed = parser.parse_args()

	if parsed.no_clobber:
		perm = 'ab'
	if parsed.outfile:
		outfile = parsed.outfile

	for file in glob.glob(parsed.filename):
		for item in parsemimikatzoutput(file):
			if item not in writetofile and item['UserName']:
				writetofile.append(item)
	try:
		with open(outfile, perm) as fh:
			dw = csv.DictWriter(fh, fieldnames=writetofile[0].keys())
			dw.writeheader()
			for stuff in writetofile:
				dw.writerow(stuff)
	except IOError:
		print("[-]Error")
