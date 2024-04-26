import time
import seeed_dht
def tempData():

    # for DHT11/DHT22
    sensor = seeed_dht.DHT("11", 12)
    # for DHT10
    # sensor = seeed_dht.DHT("10")
    
    _humi, temp = sensor.read()
    
    print(temp)
    
    return temp

