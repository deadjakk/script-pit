import threading,queue
import sys
from socket import *

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print("invalid arg num\nusage: {} <list of ips> <optional:number of threads>".format(sys.argv[0]))
	sys.exit(1)

ips = []
thread_num = 1

if len(sys.argv) == 3:
	thread_num = int(sys.argv[2])	
q=queue.Queue()
fh = open(sys.argv[1],'r')

def check_system(ip):
	port = 2701
	s = socket(AF_INET,SOCK_STREAM)
	s.connect((ip,port))
	data = s.recv(50)
	if b'\x00S\x00T\x00A\x00R\x00T\x00_\x00H\x00A\x00N\x00D\x00S\x00H\x00A\x00K\x00E\x00\x00\x00' in data:
		print("possible ca server-> {}".format(ip))

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
