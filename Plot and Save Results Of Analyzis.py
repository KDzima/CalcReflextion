import os
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import interpolate

Params=np.genfromtxt('Parameters.txt',skip_header=1)
FolderList=os.listdir('Data\\')
WavelengthArray=np.sort(Params[:,0])
R_array=np.zeros(len(WavelengthArray))
R_error_array=np.zeros(len(WavelengthArray))
V_array=np.zeros(len(WavelengthArray))
V_error_array=np.zeros(len(WavelengthArray))
for i,wave in enumerate(WavelengthArray):
    FolderPath='Data\\'+str(wave)+'\\'
    R_raw=np.loadtxt(FolderPath+'Reflection_by_integral.txt')
    V_raw=np.loadtxt(FolderPath+'V.txt')
    R_array[i]=np.nanmean(R_raw)
    R_error_array[i]=np.nanstd(R_raw)
    V_array[i]=np.nanmean(V_raw)
    V_error_array[i]=np.nanstd(V_raw)
    
np.savetxt('Reflection.txt',np.column_stack((WavelengthArray,R_array,R_error_array)))
np.savetxt('Velocity.txt',np.column_stack((WavelengthArray,V_array,V_error_array)))

plt.figure(1)
plt.errorbar(WavelengthArray,R_array,yerr=R_error_array)
plt.xlabel('Wavelength, nm')
plt.ylabel('Reflection')
plt.tight_layout()

plt.figure(2)
plt.errorbar(WavelengthArray,V_array,yerr=V_error_array)
plt.xlabel('Wavelength, nm')
plt.ylabel('Velocity, mm/ns')
wav_0=1531.47
V_theory=3e8/1.45*np.sqrt(2*(wav_0-WavelengthArray)/wav_0)/1e-3*1e-9
plt.plot(WavelengthArray,V_theory)
plt.tight_layout()
    
    
    
    
    
    