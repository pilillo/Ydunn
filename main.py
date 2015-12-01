from bitalino import *
import matplotlib.pylab as plt
import pandas as pd
import numpy as np


class Processor(object):
    # Python API at http://bitalino.com/pyAPI/
    mapping = [('EMG',1000), ('EDA',10), ('ECG',100), ('ACC',100), ('LUX',10)]
  
    def __init__(self, mac=None):
        if mac is not None:
            self.device = Bitalino(mac)
        
    def discover(self):
        return [d for d in find() if d[1]=='bitalino']

    def open(self, mac):
        self.device = BITalino(mac) 

    def get_mapping(self, channel_name):
        for i, m in enumerate( Processor.mapping ):
            if channel_name == m[0]:
                return (i, m[1])

    def start_aquisition(self, inputs):
        pins = []
        frequency = 10
        for inp in inputs:
            i, f = self.get_mapping(inp)
            pins.append(i)
            if f > frequency:
                frequency = f
        self.device.start(frequency, pins)
        
    def read(self, samples):
        return self.device.read(samples)
    
    def stop_aquisition(self):
        self.device.stop()
        self.device.close()

if __name__ == "__main__":
    p = Processor()
    try:
        p.open('98:D3:31:80:47:FB')
        p.start_aquisition(['ACC'])
        
        line, = plt.plot(range(1000))
        plt.ion()
        plt.ylim([0,10])
        plt.show()
        
        import time
        while True:
            df = pd.DataFrame(p.read(1000), columns=['index']+[c[0] for c in Processor.mapping])
            df.drop('index', axis=1, inplace=True)
            #plt.plot(df)
            #plt.draw()
            #ax.clear()
            #ax.plot(df.index, df['ACC'].tolist())
            #fig.canvas.draw()
            #plt.plot(df)
            line.set_ydata(df['ACC'].tolist())
            plt.draw()
            time.sleep(0.1)
            plt.pause(0.0001)
    except Exception as e:
        print e
    else:
        p.stop_aquisition()
