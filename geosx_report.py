import h5py 
import matplotlib.pyplot as plt
import numpy as np 

class geosx_report:
    def init(self):
        pass
      
    #file name with hdf5 format
    def get_pressure(self,file_name,path=None):
        
        with h5py.File(file_name,'r') as hdf:
            ls=list(hdf.keys())
            pressure=hdf.get('pressure')
            time=hdf.get('pressure Time')
            self.pressure=np.array(pressure)
            self.time=np.array(time)
    def get_rate(self,file_name,path=None):
        
        with h5py.File(file_name,'r') as hdf:
            ls=list(hdf.keys())
            rate=hdf.get('wellElementMixtureConnectionRate')
            time=hdf.get('wellElementMixtureConnectionRate Time')
            self.rate=np.array(rate)
            self.time=np.array(time)        
    
    def plot_well_pressure(self,file_name,well_name=None):
        inDays = 1.0 / (24 * 3600) 
        self.get_pressure(file_name)
        t= inDays*self.time[:,0]
        plt.grid()
        plt.xlabel('time [days]')
        plt.ylabel('pressure(bar)')
        plt.title(f"pressure of {well_name}")
        plt.plot(t,self.pressure[:,0]/100000) 
        return plt.show()
        
    def All_Wells_pressure(self,files_name):
        fig, ax = plt.subplots()
        ax.set_xlabel('time [days]')
        ax.set_ylabel('pressure(bar)')
        ax.set_title(f"pressure of wells")
        for file in files_name:
            self.get_pressure(file)
            inDays = 1.0 / (24 * 3600) 
            t= inDays*self.time[:,0]
            ax.plot(t,self.pressure[:,0]/100000)   
        plt.grid()
        return plt.show()
    
    def well_rate(self,file_name,well_name=None):
        inDays = 1.0 / (24 * 3600) 
        self.get_rate(file_name)
        t= inDays*self.time[:,0]
        plt.grid()
        plt.xlabel('time [days]')
        plt.ylabel('rate(CM/day)')
        inCubicMeters = 1 / 848.9
        if well_name!=None:
            plt.title(f"rate of {well_name}")
        
        plt.plot(t,abs(self.rate[:,0])* inCubicMeters / inDays) 
        plt.ylim(0, np.max(abs(self.rate[:,0])* inCubicMeters / inDays)+800)
        return plt.show()
        
    def All_Wells_rate(self,files_name):
        fig, ax = plt.subplots()
        ax.set_xlabel('time [days]')
        ax.set_ylabel('rate(CM/day)')
        ax.set_title(f"rate of wells")
        i=1
        for file in files_name:
            self.get_rate(file)
            inCubicMeters = 1 / 848.9
            inDays = 1.0 / (24 * 3600) 
            t= inDays*self.time[:,0]
            ax.plot(t,abs(self.rate[:,0])* inCubicMeters / inDays,
                 '-o',
                 label=f"Well {i}")
            i=1+i
        plt.legend(bbox_to_anchor=(0,1), loc='upper left', borderaxespad=0.1)
       
        plt.ylim(0, np.max(abs(self.rate[:,0])* inCubicMeters / inDays)+800)
        plt.grid()
        return plt.show()

sim=geosx_report()
#sim.plot_well_pressure(file_name="pressure_history.hdf5")
sim.All_Wells_rate(files_name=["wellRateHistory1.hdf5","wellRateHistory2.hdf5","wellRateHistory3.hdf5","wellRateHistory4.hdf5"])
        