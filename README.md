# script-pit
Few quick and dirty scripts that I find extremely useful on engagments, frequently used.
Will try and keep a short description of everything listed below.

## parsemimi.py
Simple script that parses mimikatz output, can be used from CLI or as an import.   
To clarify: this parses the sekurlsa::logonPasswords command's OUTPUT only. Nothing else.
Primary use-case for this is when you're finding yourself with dozens or hunreds of mimikatz logonPasswords output files.
This can parse the unique credentials so they can be placed in CSV for quick filtering/reading.

## nmap-parser.py
Parses the .nmap file for hosts that have any information containing the provided substring.  
There are a number of NMAP output parsers out there but they all seem to favor the XML format which I find lacks the output of some scripts.  
example command:
`./nmap-parser.py vuln-test.nmap <search string>`
example output:
```
$ ./nmap-parser.py vuln-test.nmap VULN
[INFO]Host: 192.168.1.28 Port: 445 --- |   VULNERABLE:
[INFO]Host: 192.168.1.28 Port: 445 --- |     State: VULNERABLE
[INFO]Host: host-0.test.local (192.168.1.29) Port: 445 --- |   VULNERABLE:
[INFO]Host: host-0.test.local (192.168.1.29) Port: 445 --- |     State: VULNERABLE
```
## parse-ips.py
Outputs unique IP addresses from files or piped stdin, works great with nmap-parser.py script above.  
Example use case using both:
```
# example of output from previous command to be piped in following command
└──╼ \>./nmap-parser.py test-nmap-scan.nmap 53 
[PORT]Host: 192.168.43.34 Port: 53/tcp open  domain
[PORT]Host: 192.168.43.199 Port: 53/tcp open  domain

# reading piped data
└──╼ \>./nmap-parser.py test-nmap-scan.nmap 53 | ./parseips.py 
192.168.43.34
192.168.43.199

# reading from file
./parseips.py test-nmap-scan.nmap 
192.168.43.0
192.168.43.34
192.168.43.198
192.168.43.199
```
## decrypt-android-react.py
Run the script in the shared_prefs directory of an android app written in React Native, you should see
the RN_KEYCHAIN.xml and crypto.KEY_256.xml in the shared_prefs directory  
```
$ python3 ./decrypt-android-react.py --help
usage: decrypt-android-react.py [-h] [--dir DIR]

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   path to shared_prefs directory  


python3 ./decrypt-android-react.py --dir com.app.whatever/shared_prefs/
```
