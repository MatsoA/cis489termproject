
import socket

UDP_IP = "192.168.43.255"
UDP_PORT = 5005

device_sensors = ['audio']

#TODO: store sensor history periodically 
data_history = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
sock.bind((UDP_IP, UDP_PORT))

#check if we have sensor and send data
def ed_respond(route, server):
	route = route.decode('utf-8')

	try:
		location, time, sensor = route.split('/')
	except:
		print("invalid route")
		#not valid route, we don't do anything else
		return 
	
	print(sensor)
	
	if sensor in device_sensors:
		data = audio_sensor()
		sock.sendto(data, (UDP_IP, UDP_PORT))
		print("data sent")
		
	#if we don't have data, simply do nothing

def audio_sensor():
	#TODO: actually interface with audio sensor
	
	return b"audio!!"

while True:
	route, server = sock.recvfrom(1024)
	
	ed_respond(route, server)
	


