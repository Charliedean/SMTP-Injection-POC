import ssl
import sys
import socket

s = socket.socket()
ServerStatus = ''

try:
	IP = sys.argv[1]
	PORT = int(sys.argv[2])
except:
	print 'python smtpinectiontest [HOST] [PORT]'
	sys.exit(1)

try:
	s.connect((IP, PORT))
	print s.recv(1024),
except:
	print 'Error Connecting'
	sys.exit(1)


s.send('STARTTLS\r\nRSET\r\n')
First = s.recv(1024)
print First,

if '220 ready for tls' in First:
	ServerStatus = '\033[92mNot Vulnerable\033[0m'
	ws = ssl.wrap_socket(s)
	Second = ws.recv(1024)
	if '250 flushed system and ready for new session' in Second:
		ServerStatus = '\033[91mVunerable\033[0m'
		print Second,
else:
	print 'Invalid Response from SMTP',
	sys.exit(1)

if ServerStatus:
	print 'Server is ' + ServerStatus
	ws.close()
