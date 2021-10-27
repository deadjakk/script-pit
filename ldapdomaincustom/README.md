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


## groupmanager.py
adds and removes a given user to a given group

```
$ python groupmanager.py  --server 192.168.1.60 --username administrator --password Password1 --domain sprawl.local --groupdn "CN=Domain Admins,CN=Users,DC=sprawl,DC=local" --userdn "CN=lowpriv lowpriv,CN=Users,DC=sprawl,DC=local" --delete
bind successful
result of delete: True
```
