import ldap3
server = ldap3.Server('<DC-IP>',get_info=ldap3.ALL)
person = ldap3.ObjectDef('inetOrgPerson')
conn = ldap3.Connection(server, user="example.com\\username", password="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", authentication=ldap3.NTLM)
conn.bind()
result = conn.delete('cn=USERNAMETODELETE,cn=Users,dc=EXAMPLE,dc=ORG')
print("user was deleted: {}".format(result)
conn.unbind()
