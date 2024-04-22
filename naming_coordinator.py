import sys
import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,    
                     socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((UDP_IP, UDP_PORT))

class Naming:
    semantic_map = {
        "studyable": ["audio", "video", "temperature"],
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
        #broadcast route to all ED
        sock.sendto(bytes(route, encoding='utf-8'), ('192.168.43.255', UDP_PORT))

        chosen_ed = "none"
        networking = "discovering"

        ed_response = "none"

        #print(networking)

        while (True):
            #print(networking)
            data, addr = sock.recvfrom(1024)
            print(data)

            if (data == b"ready"): 

                sock.sendto(bytes('true', encoding='utf-8'), (str(addr[0]), UDP_PORT))
                break

        networking = "waiting for data"

        while (networking == "waiting for data"):
            data, addr = sock.recvfrom(1024)
            
            print(data)
            networking == "discovering"
        
        


    def broadcast_request_and_receive(sub_routes):
        Naming.collision_avoidance('library/now/audio')
            

Naming.serve_route(sys.argv[1])