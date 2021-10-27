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
    },
    3:{
    "name":"exchange servers",
    "filter":"(&(objectCategory=computer)(servicePrincipalName=exchangeMDB*))",
    "properties":"*"
    },
    4:{
    "name":"unconstrained delegation",
    "filter":"(userAccountControl:1.2.840.113556.1.4.803:=524288)",
    "properties":"*"
    },
    5:{
    "name":"no kerb preauth required (asrep roast-able)",
    "filter":"(userAccountControl:1.2.840.113556.1.4.803:=4194304)",
    "properties":"*"
    }
}
