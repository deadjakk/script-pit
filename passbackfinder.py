import threading,queue
import requests as r
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if len(sys.argv) != 2 and len(sys.argv) != 3:
	print("invalid arg num\nusage: {} <list of ips with port 443> <optional:number of threads>".format(sys.argv[0]))
	sys.exit(1)
ips = []
thread_num = 1
if len(sys.argv) == 3:
	thread_num = int(sys.argv[2])	
q=queue.Queue()
fh = open(sys.argv[1],'r')

def check_system(ip):
	url ="https://{}/properties/index.php".format(ip)
	print("trying {}".format(ip))
	resp = r.get(url,verify=False,timeout=5)
	print(resp.status_code)
	if resp.status_code == 200 and "XEROX" in resp.text.upper():
		print("{} may be vulnerable -> {}".format(ip,url))


# reading hosts in to a list
for line in fh.readlines():
	line=line.strip()
	if line not in ips:
		ips.append(line)

def worker():
	while True:
		ip = q.get()
		try:
			check_system(ip)	
		except Exception as e:
			print("error checking system: {}".format(e),file=sys.stderr)
		q.task_done()

print ("running with {} threads against {} host(s)".format(thread_num,len(ips)))

for ip in ips:
	q.put(ip)

for n in range (0,thread_num):
	threading.Thread(target=worker,daemon=True).start()
	print ("started thread")

q.join()
print("finished")
sys.exit(0)
