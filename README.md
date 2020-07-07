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
