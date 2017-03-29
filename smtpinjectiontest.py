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
First = s.recv(1024).strip()
print First

if First.startswith('220'):
	ServerStatus = '\033[92mNot Vulnerable\033[0m'
	ws = ssl.wrap_socket(s)
	Second = ws.recv(1024).strip()
	if Second.startswith('250'):
		ServerStatus = '\033[91mVunerable\033[0m'
		print Second
else:
	print 'Invalid Response from SMTP',
	sys.exit(1)

if ServerStatus:
	print 'Server is ' + ServerStatus
	ws.close()
