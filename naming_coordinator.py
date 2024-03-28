import sys

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
            #TODO: code to broadcast http request with subroute 
            pass

        #TODO: recieve data and return all output recieved
        #TODO: filter responses of the same topic (choose one)

        #for testing
        print(sub_routes) 
    
    


#test usage:
Naming.serve_route(sys.argv[1])
