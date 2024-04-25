import pyaudio
import time
from math import log10
import audioop  

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())
# Fragment = in_data
def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

def audioReturn():
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    input_device_index=DEVICE,
                    channels=1,
                    rate=RATE,
                    input=True,
                    output=False,
                    stream_callback=callback)

    stream.start_stream()
    my_list = []
    testN = 0
    while stream.is_active() and testN != 15: 
        db =  20*log10(rms)
        if len(my_list) <= 6:
            my_list.append(float(db))
        else:
            my_list = my_list[1:]
            print("done")
            return bytes(str("audio:{}".format(sum(my_list)/len(my_list))), encoding = "utf-8")
            my_list.clear()
        
        print(f"Sensing ... RMS: {rms} DB: {db}") 
        # refresh every 0.3 seconds 
        time.sleep(1)
        
        #print(my_list)
        testN += 1
    stream.stop_stream()
    stream.close()
    
    #TODO: Remove
    p.terminate()
