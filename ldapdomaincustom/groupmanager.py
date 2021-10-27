import ldap3, argparse, sys
# <3 https://stackoverflow.com/questions/44609358/ldap3-python-add-user-to-group
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups 
from ldap3.extend.microsoft.removeMembersFromGroups import ad_remove_members_from_groups 
from ldap3.utils.dn import safe_dn
from ldap3.core.exceptions import LDAPInvalidDnError, LDAPOperationsErrorResult
from types import GeneratorType

# main
parser = argparse.ArgumentParser()
parser.add_argument("--domain",help="domain for authenticating user",
        required=True)
parser.add_argument("--username",help="user for authenticating password", 
        required=True)
parser.add_argument("--password",help="password or full ntlm hash to "
        "authenticating account", required=True)
parser.add_argument("--server",help="dc ip ")
parser.add_argument("--groupdn",help="distinguished name of group where user "
        "should be added",required=True)
parser.add_argument("--userdn",help="distinguished name of user to add "
        "to group",required=True)
parser.add_argument("--delete",help="delete user from group, rather than add "
        "if delete is not specified, default action is add",action="store_true")
args = parser.parse_args()

server = ldap3.Server(args.server,get_info=ldap3.ALL)
conn = ldap3.Connection(server, user="{}\\{}".format(args.domain,args.username),
        password=args.password,authentication=ldap3.NTLM)

if not conn.bind():
    print("could not bind successfully")
    sys.exit(1)
print("bind successful")

user_dn=[args.userdn]
group_dn=[args.groupdn]

if args.delete:
    result=ad_remove_members_from_groups(conn, user_dn, group_dn,fix=True)
    print("result of delete: {}".format(result))
else:
    result=ad_add_members_to_groups(conn, user_dn, group_dn)
    print("result of add: {}".format(result))

conn.unbind()
