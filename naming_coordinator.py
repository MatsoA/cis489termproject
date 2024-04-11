import sys
import socket

UDP_IP = "192.168.43.255"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

class Naming:
    semantic_map = {
        "studyable": ["audio", "video", "temperature"],
        "numPeople": ["video"]
    }

    #to be populated as devices connect
    devices = []


    def serve_route(route):
        #location/time/semantic -> [location, time, semantic]
        location, time, semantic = route.split("/")

        #list of subroutes we need to request to gather all the information needed to answer semantic route  
        sub_routes = ["{}/{}/{}".format(location, time, topic) for topic in Naming.semantic_map[semantic]]

        return Naming.broadcast_request_and_receive(sub_routes)


    def broadcast_request_and_receive(sub_routes):
        for route in sub_routes:
            # code to broadcast http request with subroute
            sock.sendto(bytes(route, encoding='utf-8'), (UDP_IP, UDP_PORT))

        sock.bind((UDP_IP, UDP_PORT))
        # recieve data and return all output recieved
        while True:
            data, addr = sock.recvfrom(1024)
            return data
        # filter responses of the same topic (choose one)

        #for testing
        print(sub_routes) 

#test usage:
Naming.serve_route(sys.argv[1])
