# script-pit
Obligatory repo for one off scripts and such that i've written, useful on engagements and whatnot.
Will try and keep a short description of everything listed below.

## parsemimi.py
Simple script that parses mimikatz output, can be used from CLI or as an import.

## nmap-parser.py
Parses the .nmap file for hosts that have any information containing the provided substring.  
example command:
`./nmap-context-parser.py vuln-test.nmap <search string>`
example output:
```
$ ./nmap-context-parser.py vuln-test.nmap VULN
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
