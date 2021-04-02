#!/usr/bin/python3
from base64 import b64decode as decode
import Cryptodome.Cipher.AES as AES
import xmltodict
import argparse
"""
Author: @deadjakk

Usage:

Run the script in the shared_prefs directory of an 
android app written in React Native, you should see
the RN_KEYCHAIN.xml and crypto.KEY_256.xml in the
shared_prefs directory

"""

parser = argparse.ArgumentParser()
parser.add_argument('--dir',help='path to shared_prefs directory',default='./')
args=parser.parse_args()

keychain=   (args.dir+'/RN_KEYCHAIN.xml')
keycontent= (args.dir+'/crypto.KEY_256.xml')

# decrypts.... um things
def decryptthing(k,thing):
    thing = decode(thing)
    n = 14
    iv = thing[ 2:n ]  
    xcrypted = thing[ n: ] 
    a=AES.new(k, AES.MODE_GCM, iv)      
    print ( a.decrypt(xcrypted) )

# read the XML files
with open(keychain,'r') as fh:
    keychainxml = fh.read()
with open(keycontent,'r') as fh:
    keycontent = fh.read()

keychaindict = xmltodict.parse(keychainxml)
keycontentdict = xmltodict.parse(keycontent)

# parse the key
for item in  keycontentdict['map']['string']:
    k = keycontentdict['map']['string'][item]

print ('using key: {}'.format(k))
k = decode(k)

# decrypt things
for item in  keychaindict['map']['string']:
    for value in item.values():
        if value[:2] == 'AQ':
            decryptthing(k,value)
        else:
            print('decrypting',value,end='---> ')

