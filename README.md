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

## ldd.py (fork of ldapdomaindump for custom queries)
A small fork of ldapdomaindump that allows for use of custom one-off queries
using the --query and --props flags, as well as batch queries using the --batch
flag directing it to a query.py file containing a dictionary with the query info.  

output formatting is only raw right now, and has not yet been fixed.  
```
$ cat queries.py
queries={
    1:{
    "name":"file servers",
    "filter":"(&(samAccountType=805306368)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(homedirectory=*)(scriptpath=*)(profilepath=*)))",
    "properties":"homedirectory,scriptpath,profilepath"
    },
    2:{
    "name":"all users, all properties",
    "filter":"(objectClass=user)",
    "properties":"*"
    }
}

$ python3 ldd.py -o ldap -u sprawl.local\\administrator -p Password1 sprawl.local --batch queries.py
[*] Connecting to host...
[*] Binding to host
[+] Bind OK
[*] Starting domain dump
available queries:
1 : file servers
2 : all users, all properties
enter index of desired queries, (comma delimited numbers are accepted as well)
example: 1,3,5
>1,2
[DN: CN=user2,CN=Users,DC=sprawl,DC=local - STATUS: Read - READ TIME: 2021-10-26T18:50:45.506744
    accountExpires: 1601-01-01 00:00:00+00:00
    badPasswordTime: 1601-01-01 00:00:00+00:00
    badPwdCount: 0
    cn: user2
    ...
```
