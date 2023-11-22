#!/usr/bin/env python
HELP_TEXT="""author: deadjakk
Useful if you are constantly having a socks proxy drop and interrupt your scans or something.
Basically you give this an address that you know should be accessible through the proxy via the '-s' argument.
Then you give this an the sockaddr of the part of the proxy chain that keeps droppping via the '-p' argument.
Finally you give it the command that you are trying to run; probably nmap or whatever you are using.

When the proxychain times out it will suspend the command you ran until the proxy is re-established, at which point
it will resume the process.

NOTE: You will need to wrap the entire command in proxychains, not the command argument.
ANOTHER NOTE: Do not run proxychains with -q, it must see the annoying chainlines
EXAMPLE: 
    proxychains4 python3 suspendwatcher.py -p 127.0.0.1:9998 -s 1.1.1.1:80 nmap example.com
"""
import sys
import os
import subprocess
from time import sleep
import psutil
from socket import *
from argparse import ArgumentParser

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = ArgumentParser(description=HELP_TEXT)
parser.add_argument("-v", help="verbose output", action="store_true")
parser.add_argument("-s", "--sockaddr", help="sock addr to watch, ex: 1.1.1.1:8000 this is something that should always be open", required=True)
parser.add_argument("-p", "--proxyaddr", help="sock addr to watch, ex: 1.1.1.1:8000 this is something that should always be open", required=True)
parser.add_argument("command", help="command to run, can be anything", nargs='*')
args = parser.parse_args()

def await_sockaddr(sockaddr, args):
    ssockaddr = sockaddr.split(":")
    host, port = ssockaddr[0], int(ssockaddr[1])
    while 1:
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((host,port))
            # it must be back up, let's resume the process
            break
        except Exception as e:
            if args.v:
                print(f"error connecting to {sockaddr}: {e}")
        sleep(5)

with subprocess.Popen(args.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
    print(f"{colors.GREEN}started process ({process.pid}): {args.command}{colors.END}")
    p = psutil.Process(process.pid)
    try:
        while process.poll() is None:
            data = process.stderr.read() 
            sys.stdout.flush()
            if f"{args.proxyaddr}  ...  timeout".encode() in data:
                p.suspend()
                print(f"{colors.RED}SUSPENDED PROCESS{colors.END}")
                await_sockaddr(args.sockaddr, args)
                p.resume()
                print(f"{colors.GREEN}RESUMED PROCESS{colors.END}")
    except KeyboardInterrupt:
        print(".", end='')
        exit(0)
