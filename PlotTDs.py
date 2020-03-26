import os
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import interpolate

Params=np.genfromtxt('Parameters.txt',skip_header=1)
FolderList=os.listdir('Data\\')
WavelengthArray=Params[:,0]
for i,wave in enumerate(WavelengthArray):
    print(wave)
    FolderPath='Data\\'+str(wave)+'\\'
    SignalArray=np.loadtxt(FolderPath+'TDArray.txt')
    Positions=np.loadtxt(FolderPath+'TD_Positions.txt')
    TimeArray=np.loadtxt(FolderPath+'TimesArray.txt')
    
    
    TimeArray-=TimeArray[np.argmax(SignalArray[:,0])]
    SignalArray-=np.mean(SignalArray,0)
    Positions_in_mkm=(Positions[:,1]-Positions[-1,1])*2.5
        
   
    plt.figure(2)
    plt.clf()
    plt.contourf(Positions_in_mkm,TimeArray,SignalArray,200,cmap='RdBu_r')
    plt.colorbar().set_label('Intensity, arb.u.')
    plt.xlabel('Distance, um')
    plt.ylabel('Time, s')
    plt.ylim([-0.5e-9,5e-9])
    plt.savefig('PICS\\'+str(wave)+'.png',dpi=300)
    
    