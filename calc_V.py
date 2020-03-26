# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:25:52 2020

@author: Dima
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import interpolate
from scipy import signal


def calculateCenter(X,Y):
    return np.sum(X*Y)/np.sum(Y)

window_to_calculate_v=10
SNR_desired=5
TimeShiftConstant=2.45e-8
Params=np.genfromtxt('Parameters.txt',skip_header=1)
FolderList=os.listdir('Data\\')

for i,wave in enumerate(Params[:,0]):
    FolderPath='Data\\'+str(wave)+'\\'
    SignalArray=np.loadtxt(FolderPath+'TDArray.txt')
    TimeArray=np.loadtxt(FolderPath+'TimesArray.txt')
    Positions=np.loadtxt(FolderPath+'TD_Positions.txt')  
    Z=(Positions[:,1]-Positions[-1,1])*2.5
    
    t_min=-0.5e-9+TimeShiftConstant
    i_min=np.argmin(abs(TimeArray-t_min))
    
    t_medium=Params[i,2]*1e-8
    i_medium=np.argmin(abs(TimeArray-t_medium))
    
    t_max=TimeArray[np.argmax(SignalArray[i_medium:-1,0])+i_medium]+0.5e-9
    i_max=np.argmin(abs(TimeArray-t_max))
    
      
    TD_2=SignalArray[i_medium:i_max,0:window_to_calculate_v]
    TD_1=SignalArray[i_min:i_medium,0:window_to_calculate_v]
    TD_noise=SignalArray[i_max:-1,0:window_to_calculate_v]
    
    
    V=list()
    for k in range(len(TD_1[0,:])):
        noise=np.mean(TD_noise[:,k])
        if (np.max(TD_1[:,k])/noise>SNR_desired) and (np.max(TD_2[:,k])/noise>SNR_desired):
            t2=calculateCenter(TimeArray[i_medium:i_max],TD_2[:,k])
            t1=calculateCenter(TimeArray[i_min:i_medium],TD_1[:,k])
            V_current=2*(Z[k]-Z[-1])/(t1-t2)/1e3/1e9
            V.append(V_current)
    V=np.array(V)
    print('Waveelngth', wave,' Velocity mean ', np.mean(V),' std ', np.std(V))
    np.savetxt(FolderPath+'V.txt',V)
    