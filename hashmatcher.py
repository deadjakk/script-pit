#!/usr/bin/env python
import sys, os
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("input", help="the NTDS.dit dump output to parse")
parser.add_argument("-d", "--debug", help="display debug output", action="store_true")
parser.add_argument("-r", "--redact", help="redact the first N characters of the output", default="0")
parser.add_argument("-s", "--search", help="return only matched hashes shared by users with provided substring")
parser.add_argument("-l", "--limited", help="return only matched hashes shared by users with provided substring and only "
                    "return the users associated with accounts containing that substring (requires -s arg)", action="store_true")
parser.add_argument("-t", "--test-jaccard", help="runs and outputs the jaccard similarity for the limited search function", action="store_true")
parser.add_argument("-j", "--jaccard", help="set the acceptable greater than or equal jaccard similary value to denote a match"
                    "for the limited search function", default=.8888)

args = parser.parse_args()

filename = args.input
pass_dict = {}
redact = int(args.redact)

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


if os.path.exists(filename) is False:
    raise FileNotFoundError(f"{filename} not found")

with open(filename, 'r') as fh:
    for line in fh.readlines():
        if ":::" not in line:
            continue
        line = line.strip()
        sline = line.split(":")
        user = sline[0]
        hash_ = sline[3]
        if pass_dict.get(hash_, None) is None:
            pass_dict[hash_] = []
        pass_dict[hash_].append(user)

for h,arr in pass_dict.items():
    if len(arr) == 1:
        continue
    if args.search and args.limited is False:
        if any([user for user in arr if args.search in user]):
            print(f"the hash {redact*'X'}{h[redact:]} is shared by {arr}")
        continue
    elif args.limited and args.search:
        if any([user for user in arr if args.search in user]):
            filtered_users = filter_users(arr, args.search, args)
            if len(filtered_users) == 0:
                continue
            print(f"the hash {redact*'X'}{h[redact:]} is shared by {filtered_users}")
        continue
    print(f"the hash {redact*'X'}{h[redact:]} is shared by {arr}")
