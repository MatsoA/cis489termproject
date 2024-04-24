
import socket
import time
import random
import select

UDP_LISTEN = "0.0.0.0"
BROADCAST_IP = '192.168.137.255'
UDP_PORT = 5005

device_sensors = ['audio', 'temperature']

#TODO: store sensor history periodically 
data_history = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_LISTEN, UDP_PORT))

#check if we have sensor and send data
def ed_respond(route, server):
	route = route.decode('utf-8')

	wait_for_CA = True

	try:
		location, time, sensor = route.split('/')
	except:
		print("invalid route")
		#not valid route, we don't do anything else
		return 
	
	print(sensor)
	
	if sensor in device_sensors:
		print(server[0], server[1])
		sock.sendto(bytes("ready", encoding='utf-8'), (str(server[0]), server[1]))
		
		while (wait_for_CA == True):
			
			getData = select.select([sock], [], [], 5)
			
			if (getData[0]):
				data, addr = sock.recvfrom(1024)
				if (data == b"true"):
					sock.sendto(audio_sensor(), (str(server[0]), UDP_PORT))
				
				wait_for_CA = False
			#on timeout
			if (getData[0] == []):
				wait_for_CA = False
		
	#if we don't have data, simply do nothing

	return
	

def audio_sensor():
	#TODO: actually interface with audio sensor
	
	return b"audio:-4"
	
def temp_sensor():
	return b"temperature:-4"

while True:
	print('loop start')
	time.sleep(random.random())
	route, server = sock.recvfrom(1024)

	ed_respond(route, server)
	print('loop done')
