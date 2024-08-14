#!/usr/bin/env python
import sys, os
from argparse import ArgumentParser
from pathlib import Path

def is_subset(lista, listb):
    """
    check if lista is a subset of listb, does not remove duplicates
    checks the length of each character in lista to check if it is gte
    the number of that character in listb
    """
    if "\\" in lista: lista=lista.split("\\")[1]
    if "\\" in listb: listb=listb.split("\\")[1]
    if isinstance(lista,list): lista=list(lista)
    if isinstance(listb,list): listb=list(listb)
    itema_dict = {c:lista.count(c) for c in lista}
    itemb_dict = {c:lista.count(c) for c in listb}
    for k,v in itema_dict.items():
        if itemb_dict.get(k, None) is None:
            return False
        if itema_dict[k] > itemb_dict[k]:
            return False
    return True


def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

def filter_users(users, term, args):
    fusers = list()
    users = [user.lower() for user in users]
    users_with_term = [user for user in users if term in user]
    users_without_terms = [user for user in users if user not in users_with_term]
    for user_without_term in users_without_terms:
        for user_with_term in users_with_term:
            if user_without_term in fusers or user_with_term in fusers:
                continue  # one of them has already found a match
            if args.debug:
                print("[DEBUG]",user_without_term, user_with_term, is_subset(user_without_term, user_with_term))
            if is_subset(user_without_term, user_with_term.replace(term,"")) is False:
                continue
            similarity = jaccard_similarity(user_with_term, user_without_term)
            if args.test_jaccard:
                print(f"{user_without_term} - {user_with_term}: ({similarity})")
            if similarity >= float(args.jaccard):
                fusers.append(user_without_term)
                fusers.append(user_with_term)
    return fusers 


def print_shared(hash_str, users, priv_mapping, redact=0, one_line=False):
    hash_type = "NTLM" if is_lm(hash_str) is False else "LM (BAD)"
    hash_str_formatted = f"{redact*'X'}{hash_str[redact:]}"
    dusers = users
    if len(priv_mapping) > 0:
        dusers = list()
        for user in users:
            dusers.append(f"{user} {is_domain_admin(user, priv_mapping)}")

    if one_line is True:
        users_string = " and ".join(dusers)
        print(f"the {hash_type} hash: {hash_str_formatted} is shared by: {users_string}")
        return

    print(f"the hash: {hash_str_formatted} is shared by:")
    for user in dusers:
        print(f"\t{user}")


def is_lm(some_hash):
    if some_hash.split(":")[0] == "aad3b435b51404eeaad3b435b51404ee":
        return False
    return True

def is_domain_admin(user, mapping):
    if "\\" not in user:
        return ""
    user = "\\".join(user.split("\\")[1:])
    if len(mapping) == 0:
        return ""
    user_map = mapping.get(user.lower(), None)
    if user_map is None:
        return "UNKNOWN"
    return "ADMIN" if user_map["is_admin"] else ""


def build_mapping(file_path):
    ret_mapping = {}
    domain_users_grep_path = Path(file_path)
    lines = domain_users_grep_path.read_text().splitlines()
    for line in lines:
        sline = line.split("\t")
        if not sline:
            continue
        if len(sline) < 3:
            continue
        samaccountname = sline[2].lower()
        is_admin = "Domain Admins" in line or "Enterprise Admins" in line
        ret_mapping[samaccountname] = { "is_admin": is_admin }
    return ret_mapping

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", help="the NTDS.dit dump output to parse")
    parser.add_argument("-d", "--debug", help="display debug output", action="store_true")
    parser.add_argument("-a", "--admin-mapping", help="file path to domain_users.grep to show if users are admin or filter on admins")
    parser.add_argument("-o", "--one-line", help="print one line for each hash", action="store_true", default=False)
    parser.add_argument("-r", "--redact", help="redact the first N characters of the output", default="0")
    parser.add_argument("-s", "--search", help="return only matched hashes shared by users with provided substring in their username")
    parser.add_argument("-l", "--limited", help="return only matched hashes shared by users with provided substring and only "
                        "return the users associated with accounts containing that substring (requires -s arg)", action="store_true")
    parser.add_argument("-t", "--test-jaccard", help="runs and outputs the jaccard similarity for the limited search function", action="store_true")
    parser.add_argument("-j", "--jaccard", help="set the acceptable greater than or equal jaccard similary value to denote a match"
                        "for the limited search function", default=.8888)

    args = parser.parse_args()

    domain_priv_mapping = {}
    if args.admin_mapping:
        domain_priv_mapping = build_mapping(args.admin_mapping)
    filename = args.input
    pass_dict = {}
    args.redact = int(args.redact)

    if os.path.exists(filename) is False:
        raise FileNotFoundError(f"{filename} not found")

    with open(filename, 'r') as fh:
        for line in fh.readlines():
            if ":::" not in line:
                continue
            line = line.strip()
            sline = line.split(":")
            user = sline[0]
            hash_ = ":".join([sline[2], sline[3]])
            if pass_dict.get(hash_, None) is None:
                pass_dict[hash_] = []
            pass_dict[hash_].append(user)


    for hash_str, users_array in pass_dict.items():
        if len(users_array) < 2:
            continue

        if args.limited:
            assert args.search, "-s parameter must be provided with -l"
            if any([user for user in users_array if args.search in user]):
                filtered_users = filter_users(users_array, args.search, args)
                if len(filtered_users) == 0:
                    continue
                print_shared(hash_str, filtered_users, domain_priv_mapping, args.redact, args.one_line)
            continue

        if args.search and any([user for user in users_array if args.search in user]):
            print_shared(hash_str, users_array, domain_priv_mapping, args.redact, args.one_line)
            continue

        print_shared(hash_str, users_array, domain_priv_mapping, args.redact, args.one_line)
