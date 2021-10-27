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
