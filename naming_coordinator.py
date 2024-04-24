import sys
import socket
from datetime import datetime, timedelta
import select
UDP_IP = '0.0.0.0'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,    
                     socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((UDP_IP, UDP_PORT))

class Naming:
    semantic_map = {
        "studyable": ["video", "audio", "temperature"],
        "numPeople": ["video"]
    }

    #to be populated as devices connect
    devices = []

    #state variable for networking
    networking = "idle"


    def serve_route(route):
        #location/time/semantic -> [location, time, semantic]
        location, time, semantic = route.split("/")

        #list of subroutes we need to request to gather all the information needed to answer semantic route  
        sub_routes = ["{}/{}/{}".format(location, time, topic) for topic in Naming.semantic_map[semantic]]

        return Naming.broadcast_request_and_receive(sub_routes)


    def collision_avoidance(route):
        location, time, sensor = route.split("/")

        #broadcast route to all ED
        sock.sendto(bytes(route, encoding='utf-8'), ('192.168.137.255', UDP_PORT))

        chosen_ed = "none"
        networking = "discovering"

        ed_response = "none"

        #print(networking)

        while (True):
            #print(networking)

            found = select.select([sock], [], [], 5)

            if (found[0]): 
                data, addr = sock.recvfrom(1024)
                print("57, {}".format(data))

                if (data == b"ready"): 
                    sock.sendto(bytes('true', encoding='utf-8'), (str(addr[0]), UDP_PORT))
                    break
            else:
                return 'no device'

        while (True):
            print("waiting for data")
            getData = select.select([sock], [], [], 15)

            if (getData[0]):

                response, addr = sock.recvfrom(1024)
                
                response = str(response, encoding='utf-8')
            
                try:
                    tag, data = response.split(':')
                    if (str(tag) == sensor):
                        return data
                except:
                    pass

            print("data received?")        
            
            if (getData[0] == []):
                return "no data"

            
        
        


    def broadcast_request_and_receive(sub_routes):
        output = {}

        for route in sub_routes:
            location, time, semantic = route.split('/')

            output[semantic] = Naming.collision_avoidance(route)

        return output
            

print(Naming.serve_route(sys.argv[1]))