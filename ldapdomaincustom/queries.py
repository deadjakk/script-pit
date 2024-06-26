queries={
    1:{
    "name":"home directories, can be used to find file servers",
    "filter":"(&(samAccountType=805306368)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(homedirectory=*)(scriptpath=*)(profilepath=*)))",
    "properties":"homedirectory,scriptpath,profilepath,samaccountname"
    },
    2:{
    "name":"all users all properties",
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
    },
    6:{
    "name":"disabled users",
    "filter":"(&(objectclass=user)(objectcategory=user)(useraccountcontrol:1.2.840.113556.1.4.803:=2))",
    "properties":"*"
    },
    7:{
    "name":"all groups all properties",
    "filter":"(objectClass=group)",
    "properties":"*"
    },
    8:{
    "name":"description,notes,jobtitles",
    "filter":"(&(objectClass=user)(|(description=*)(notes=*)))",
    "properties":"samaccountname,description,notes,title"
    },
    9:{
    "name":"useful computer info ",
    "filter":"(objectClass=computer)",
    "properties":"dNSHostName,samaccountname,operatingsystem,lastLogon,isCriticalSystemObject,name,servicePrincipalName,operatingSystemVersion"
    },
    10:{
    "name":"dumplaps",
    "filter":"(&(objectCategory=computer)(ms-MCS-AdmPwd=*))",
    "properties":"ms-MCS-AdmPwd,SAMAccountname,ms-Mcs-AdmPwdExpirationTime"
    },
    11:{
    "name":"unconstrained delegation (samAccountName + lastLogon) (no DCs)",
    "filter":"(&(userAccountControl:1.2.840.113556.1.4.803:=524288)(!(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))))",
    "properties":"samaccountname,lastLogon"
    },
    12:{
    "name":"domain controllers (samaccountonly)",
    "filter":"(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))",
    "properties":"samaccountname"
    },
}
