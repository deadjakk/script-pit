#!/usr/bin/python3
import re,sys
fh, inp, out = None, None, None
arr = []

if len(sys.argv) == 2:
    fh = open(sys.argv[1],'r')
    inp = fh.read()
    fh.close()
else:
    inp = sys.stdin.read()

try:
    out = re.findall("[\d\d\d]+\.[\d\d\d]+\.[\d\d\d]+\.[\d\d\d]+",inp)
except TypeError as e:
    print("Err:{}".format(e))
    sys.exit(0)

for item in out:
    if item not in arr:
        arr.append(item)
for x in arr:
    n = True
    try:
        for num in x.split("."):
            if int(num) > 255:
                n = False
                continue
        if n:
            print(x)
    except:
        pass # lol
